// Lumen Trail backend API — SAAS-140 Lesson 2 starter.
//
// End state of Lesson 1 — Redis is wired up and the /favorites/:userId endpoint
// reads a per-user set from Redis. This lesson introduces a NEW endpoint
// (/popular-routes) that is intentionally slow — it simulates a request that
// has to crunch rankings on every call. Your job is to add cache-aside: check
// Redis first, hit the slow function only on miss, then stash the result with
// a TTL.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL ?? "redis://127.0.0.1:6379");
const app = new Hono();

app.get("/health", (c) => c.json({ status: "ok" }));

// Read a user's favorite routes — end state of Lesson 1.
// Favorites are stored as a Redis Set under the key `fav:<userId>`.
app.get("/favorites/:userId", async (c) => {
  const userId = c.req.param("userId");
  const routeIds = await redis.smembers(`fav:${userId}`);
  return c.json({ userId, favorites: routeIds });
});

// Simulated expensive ranking query. In the real Lumen Trail this would join
// routes, trips, and reviews and compute a score. For teaching we fake 800ms.
async function computePopularRoutes(): Promise<Array<{ id: string; name: string; score: number }>> {
  await new Promise((r) => setTimeout(r, 800));
  return [
    { id: "r-001", name: "Rainier Wonderland Loop", score: 94 },
    { id: "r-002", name: "Zion Narrows", score: 91 },
    { id: "r-003", name: "Angels Rest", score: 88 },
    { id: "r-004", name: "Half Dome Cables", score: 86 },
    { id: "r-005", name: "Mount Washburn", score: 82 }
  ];
}

// NO CACHING. Every call pays the 800ms.
app.get("/popular-routes", async (c) => {
  const routes = await computePopularRoutes();
  return c.json({ routes });
});

const port = Number(process.env.PORT ?? 3000);

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
