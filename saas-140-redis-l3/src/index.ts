// Lumen Trail backend API — SAAS-140 Lesson 3 starter.
//
// L3 teaches session storage. The in-memory Map in src/sessions.ts is wrong on
// purpose — two API processes split sessions by whoever answered the signin
// request. The exercises direct Claude Code to swap the Map for node-redis
// SET/GET with TTL and prove the two-process test now works.
//
// End-state from L2: /items cache-aside, invalidate on write.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { getCookie, setCookie, deleteCookie } from "hono/cookie";
import { randomBytes } from "node:crypto";
import { query } from "./db.js";
import { connectRedis } from "./redis.js";
import { getOrSet, invalidate } from "./cache.js";
import { sessions } from "./sessions.js";

await connectRedis();

const app = new Hono();

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

// Session routes — in-memory for now; L3 Exercise 3 swaps for Redis.
app.post("/signin", async (c) => {
  const body = (await c.req.json().catch(() => ({}))) as { email?: string };
  if (!body.email) return c.json({ error: "missing_email" }, 400);
  const { rows } = await query(
    "SELECT id, email FROM users WHERE email = $1",
    [body.email],
  );
  if (rows.length === 0) return c.json({ error: "no_such_user" }, 404);
  const sid = randomBytes(32).toString("hex");
  await sessions.create(sid, {
    userId: rows[0].id,
    email: rows[0].email,
    expiresAt: Date.now() + 1000 * 60 * 60 * 24,
  });
  setCookie(c, "sid", sid, { httpOnly: true, sameSite: "Lax", path: "/" });
  return c.json({ status: "ok" });
});

app.get("/me", async (c) => {
  const sid = getCookie(c, "sid");
  if (!sid) return c.json({ error: "no_session" }, 401);
  const record = await sessions.get(sid);
  if (!record) return c.json({ error: "no_session" }, 401);
  return c.json({ userId: record.userId, email: record.email });
});

app.post("/signout", async (c) => {
  const sid = getCookie(c, "sid");
  if (sid) await sessions.destroy(sid);
  deleteCookie(c, "sid", { path: "/" });
  return c.json({ status: "ok" });
});

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
