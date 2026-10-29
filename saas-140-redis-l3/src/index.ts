// Lumen Trail backend API — SAAS-140 Lesson 3 starter.
//
// End state of Lesson 2 — /popular-routes is cache-aside backed. This lesson
// introduces a toy auth flow: POST /login hands back a session id, GET /me
// looks up the user by session id, POST /logout destroys it. Sessions are
// stored in a plain in-memory Map, so every server restart logs everyone out.
// Your job is to move the session store to Redis so sessions survive restarts
// and can be shared across multiple server processes.

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
    { id: "r-002", name: "Zion Narrows", score: 91 },
    { id: "r-003", name: "Angels Rest", score: 88 }
  ];
}

app.get("/popular-routes", async (c) => {
  const cached = await redis.get("popular-routes");
  if (cached) return c.json({ routes: JSON.parse(cached), source: "cache" });
  const routes = await computePopularRoutes();
  await redis.set("popular-routes", JSON.stringify(routes), "EX", 60);
  return c.json({ routes, source: "fresh" });
});

// ---- Auth-ish bits — the subject of Lesson 3 ----

// Toy user "database" — a real app would use Postgres.
const users: Record<string, { id: string; name: string }> = {
  "alice@lumentrail.test": { id: "u-alice", name: "Alice Explorer" },
  "bob@lumentrail.test": { id: "u-bob", name: "Bob Beginner" }
};

// IN-MEMORY sessions. Dies on every server restart. YOUR JOB is to replace this.
const sessions = new Map<string, { userId: string; createdAt: number }>();

app.post("/login", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const email = typeof body?.email === "string" ? body.email : "";
  const user = users[email];
  if (!user) return c.json({ error: "unknown user" }, 401);
  const sid = randomUUID();
  sessions.set(sid, { userId: user.id, createdAt: Date.now() });
  return c.json({ sessionId: sid, user });
});

app.get("/me", (c) => {
  const sid = c.req.header("x-session-id") ?? "";
  const sess = sessions.get(sid);
  if (!sess) return c.json({ error: "no session" }, 401);
  return c.json({ userId: sess.userId });
});

app.post("/logout", (c) => {
  const sid = c.req.header("x-session-id") ?? "";
  sessions.delete(sid);
  return c.json({ ok: true });
});

const port = Number(process.env.PORT ?? 3000);

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
