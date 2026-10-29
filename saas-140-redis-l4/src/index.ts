// Lumen Trail backend API — SAAS-140 Lesson 4 starter.
//
// End state of Lesson 3 — sessions now live in Redis under the key `sess:<sid>`.
// This lesson adds a new endpoint, POST /routes, that creates a hiking route
// in a toy in-memory list. In production this would hit Postgres. The problem
// is that the endpoint is unprotected: a bad actor can call it in a tight loop
// and fill the system with junk. Your job is to add rate limiting so a single
// IP (or logged-in user) can only create a few routes per minute.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { randomUUID } from "node:crypto";
import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL ?? "redis://127.0.0.1:6379");
const app = new Hono();

app.get("/health", (c) => c.json({ status: "ok" }));

app.get("/favorites/:userId", async (c) => {
  const userId = c.req.param("userId");
  const routeIds = await redis.smembers(`fav:${userId}`);
  return c.json({ userId, favorites: routeIds });
});

async function computePopularRoutes() {
  await new Promise((r) => setTimeout(r, 800));
  return [
    { id: "r-001", name: "Rainier Wonderland Loop", score: 94 },
    { id: "r-002", name: "Zion Narrows", score: 91 }
  ];
}

app.get("/popular-routes", async (c) => {
  const cached = await redis.get("popular-routes");
  if (cached) return c.json({ routes: JSON.parse(cached), source: "cache" });
  const routes = await computePopularRoutes();
  await redis.set("popular-routes", JSON.stringify(routes), "EX", 60);
  return c.json({ routes, source: "fresh" });
});

// ---- Sessions in Redis (end state of Lesson 3) ----

const users: Record<string, { id: string; name: string }> = {
  "alice@lumentrail.test": { id: "u-alice", name: "Alice Explorer" },
  "bob@lumentrail.test": { id: "u-bob", name: "Bob Beginner" }
};

const SESSION_TTL_SEC = 7 * 24 * 60 * 60;

app.post("/login", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const email = typeof body?.email === "string" ? body.email : "";
  const user = users[email];
  if (!user) return c.json({ error: "unknown user" }, 401);
  const sid = randomUUID();
  await redis.set(`sess:${sid}`, JSON.stringify({ userId: user.id }), "EX", SESSION_TTL_SEC);
  return c.json({ sessionId: sid, user });
});

app.get("/me", async (c) => {
  const sid = c.req.header("x-session-id") ?? "";
  const raw = await redis.get(`sess:${sid}`);
  if (!raw) return c.json({ error: "no session" }, 401);
  return c.json(JSON.parse(raw));
});

app.post("/logout", async (c) => {
  const sid = c.req.header("x-session-id") ?? "";
  await redis.del(`sess:${sid}`);
  return c.json({ ok: true });
});

// ---- NEW: the endpoint you'll rate-limit ----

const routes: Array<{ id: string; name: string; createdBy: string }> = [];

app.post("/routes", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const name = typeof body?.name === "string" ? body.name : "";
  if (!name) return c.json({ error: "name required" }, 400);
  const sid = c.req.header("x-session-id") ?? "";
  const raw = await redis.get(`sess:${sid}`);
  const userId = raw ? (JSON.parse(raw).userId as string) : "anonymous";
  const route = { id: `r-${randomUUID().slice(0, 8)}`, name, createdBy: userId };
  routes.push(route);
  return c.json(route, 201);
});

app.get("/routes", (c) => c.json({ routes }));

const port = Number(process.env.PORT ?? 3000);

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
