// Lumen Trail backend API — SAAS-120 starter.
//
// This file is intentionally tiny. Every lesson of SAAS-120 adds something to it
// via Claude Code: new endpoints, request validation, error handling, docs, tests.
//
// The one baked-in endpoint is GET /health, which returns {"status":"ok"} so you
// have something to verify the server is alive before you add anything new.

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
