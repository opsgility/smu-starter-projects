// Lumen Trail backend API — SAAS-140 Lesson 1 starter.
//
// L1 is where you meet Redis itself. The API already hits Postgres for /items
// (unmeasured, uncached — on purpose). The lesson walks you through SET / GET /
// HSET / LPUSH / BLPOP from redis-cli, then has you direct Claude Code to add
// a tiny Node script that round-trips a value through node-redis v4. Nothing
// about this file touches Redis yet — that's L2's job.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { query } from "./db.js";

const app = new Hono();

app.get("/health", (c) => c.json({ status: "ok" }));

app.get("/items", async (c) => {
  const { rows } = await query<{
    id: number;
    slug: string;
    name: string;
    description: string;
    price_cents: number;
    rating: string;
  }>("SELECT id, slug, name, description, price_cents, rating FROM trail_items ORDER BY id");
  return c.json({ items: rows });
});

app.get("/items/:slug", async (c) => {
  const slug = c.req.param("slug");
  const { rows } = await query(
    "SELECT id, slug, name, description, price_cents, rating FROM trail_items WHERE slug = $1",
    [slug],
  );
  if (rows.length === 0) return c.json({ error: "not_found" }, 404);
  return c.json(rows[0]);
});

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
