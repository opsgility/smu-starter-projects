// Lumen Trail backend API — SAAS-140 Lesson 4 starter.
//
// L4 teaches rate limiting. The /items/:slug/favorite endpoint is on purpose
// UNPROTECTED — a single curl loop can hammer it a thousand times a second.
// The L4 exercises direct Claude Code to add hono-rate-limiter against the
// endpoint, keyed by the signed-in userId (falling back to client IP), with
// an INCR + TTL implementation backed by Redis.
//
// End-state from L3: /items cache-aside + invalidate on write + Redis-backed
// sessions (two API processes share the sign-in).

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { getCookie, setCookie, deleteCookie } from "hono/cookie";
import { randomBytes } from "node:crypto";
import { query } from "./db.js";
import { connectRedis } from "./redis.js";
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

// TODO (L4 Exercise 2): protect this endpoint with hono-rate-limiter —
// 20 requests per 10 seconds per userId. The L4 exercises walk the full build.
app.post("/items/:slug/favorite", async (c) => {
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

// --- auth helpers (unchanged from L3) ---

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
