// Lumen Trail backend API — SAAS-140 Lesson 1 starter.
//
// This file is intentionally tiny. Lesson 1 is where you learn Redis itself — the
// key-value model, SET/GET, lists, hashes, sets. Most of the work happens in the
// redis-cli and then in a short Node script you build with Claude Code. By the end
// of the lesson this file gets a `/favorites/:userId` endpoint that reads from
// Redis, but you start from almost nothing.

import { Hono } from "hono";
import { serve } from "@hono/node-server";

const app = new Hono();

app.get("/health", (c) => {
  return c.json({ status: "ok" });
});

const port = Number(process.env.PORT ?? 3000);

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
  console.log(`Try: curl http://localhost:${info.port}/health`);
});
