// Lumen Trail backend API — SAAS-140 Lesson 2 starter.
//
// L2 teaches cache-aside. The exercises direct Claude Code to:
//   1. Fill in getOrSet() in src/cache.ts.
//   2. Wrap the /items route in it (below — see TODO).
//   3. Measure uncached vs cached latency.
//   4. Observe the stale-cache bug after a PATCH /items/:slug.
//   5. Invalidate on write.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { query } from "./db.js";
import { connectRedis } from "./redis.js";
import { getOrSet } from "./cache.js";

await connectRedis();

const app = new Hono();

app.get("/health", (c) => c.json({ status: "ok" }));

// Baseline uncached path — Exercise 1 measures this with time-curl.
app.get("/items", async (c) => {
  const { rows } = await query(
    "SELECT id, slug, name, description, price_cents, rating FROM trail_items ORDER BY id",
  );
  return c.json({ items: rows });
});

// TODO (L2 Exercise 2): rewrite this route to use getOrSet('items:all', 60, ...)
// — the baseline above should get a slash prefix like /items-uncached while this
// becomes the real /items. The exercises walk the full migration.
app.get("/items-cached", async (c) => {
  const items = await getOrSet("items:all", 60, async () => {
    const { rows } = await query(
      "SELECT id, slug, name, description, price_cents, rating FROM trail_items ORDER BY id",
    );
    return rows;
  });
  return c.json({ items });
});

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
