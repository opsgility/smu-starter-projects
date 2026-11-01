// Lumen Trail backend API — SAAS-140 Lesson 5 starter.
//
// L5 teaches pub/sub + Streams. The /signup route below LPUSHes a signup
// event onto a Redis list; src/worker.ts reads via BLPOP. The exercises walk
// you from LPUSH/BLPOP → PUBLISH/SUBSCRIBE → Streams with consumer groups
// (the only shape that survives consumer downtime).
//
// End-state from L4: rate limiting wired on /items/:slug/favorite.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { getCookie, setCookie, deleteCookie } from "hono/cookie";
import { rateLimiter } from "hono-rate-limiter";
import { randomBytes } from "node:crypto";
import { query } from "./db.js";
import { connectRedis, redis } from "./redis.js";
import { getOrSet, invalidate } from "./cache.js";
import { sessions } from "./sessions.js";

await connectRedis();

type Variables = { userId?: number; email?: string };
const app = new Hono<{ Variables: Variables }>();

app.use("*", async (c, next) => {
  const sid = getCookie(c, "sid");
  if (sid) {
    const record = await sessions.get(sid);
    if (record) {
      c.set("userId", record.userId);
      c.set("email", record.email);
    }
  }
  await next();
});

// Rate limiter — 20 req / 10s per userId (or IP if signed out).
// Uses the in-memory store by default; the exercises optionally swap for
// @hono-rate-limiter/redis for cross-process accuracy.
const favoriteLimiter = rateLimiter({
  windowMs: 10_000,
  limit: 20,
  standardHeaders: "draft-7",
  keyGenerator: (c) => String(c.get("userId") ?? c.req.header("x-forwarded-for") ?? "anon"),
});

app.get("/health", (c) => c.json({ status: "ok" }));

app.get("/items", async (c) => {
  const items = await getOrSet("items:all", 60, async () => {
    const { rows } = await query(
      "SELECT id, slug, name, description, price_cents, rating FROM trail_items ORDER BY id",
    );
    return rows;
  });
  return c.json({ items });
});

app.patch("/items/:slug", async (c) => {
  const slug = c.req.param("slug");
  const body = (await c.req.json().catch(() => ({}))) as { name?: string };
  const { rowCount } = await query(
    "UPDATE trail_items SET name = COALESCE($2, name), updated_at = NOW() WHERE slug = $1",
    [slug, body.name ?? null],
  );
  if (rowCount === 0) return c.json({ error: "not_found" }, 404);
  await invalidate("items:all");
  return c.json({ status: "ok" });
});

app.post("/items/:slug/favorite", favoriteLimiter, async (c) => {
  const userId = c.get("userId");
  if (!userId) return c.json({ error: "no_session" }, 401);
  const slug = c.req.param("slug");
  const { rows } = await query("SELECT id FROM trail_items WHERE slug = $1", [slug]);
  if (rows.length === 0) return c.json({ error: "not_found" }, 404);
  await query(
    "INSERT INTO favorites (user_id, item_id) VALUES ($1, $2) ON CONFLICT DO NOTHING",
    [userId, rows[0].id],
  );
  return c.json({ status: "ok" });
});

// New in L5 — signup fans out an event the worker drains.
app.post("/signup", async (c) => {
  const body = (await c.req.json().catch(() => ({}))) as {
    email?: string;
    display_name?: string;
  };
  if (!body.email || !body.display_name) {
    return c.json({ error: "missing_fields" }, 400);
  }
  const { rows } = await query<{ id: number; email: string }>(
    "INSERT INTO users (email, display_name) VALUES ($1, $2) " +
      "ON CONFLICT (email) DO UPDATE SET display_name = EXCLUDED.display_name " +
      "RETURNING id, email",
    [body.email, body.display_name],
  );
  await redis.lPush(
    "signup-events",
    JSON.stringify({ user_id: rows[0].id, email: rows[0].email, at: Date.now() }),
  );
  return c.json({ status: "ok", user_id: rows[0].id });
});

// --- auth helpers (unchanged from L4) ---

app.post("/signin", async (c) => {
  const body = (await c.req.json().catch(() => ({}))) as { email?: string };
  if (!body.email) return c.json({ error: "missing_email" }, 400);
  const { rows } = await query(
    "SELECT id, email FROM users WHERE email = $1",
    [body.email],
  );
  if (rows.length === 0) return c.json({ error: "no_such_user" }, 404);
  const sid = randomBytes(32).toString("hex");
  await sessions.create(sid, { userId: rows[0].id, email: rows[0].email });
  setCookie(c, "sid", sid, { httpOnly: true, sameSite: "Lax", path: "/" });
  return c.json({ status: "ok" });
});

app.post("/signout", async (c) => {
  const sid = getCookie(c, "sid");
  if (sid) await sessions.destroy(sid);
  deleteCookie(c, "sid", { path: "/" });
  return c.json({ status: "ok" });
});

app.get("/me", (c) => {
  const userId = c.get("userId");
  if (!userId) return c.json({ error: "no_session" }, 401);
  return c.json({ userId, email: c.get("email") });
});

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
