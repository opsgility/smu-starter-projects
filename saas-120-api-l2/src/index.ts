// Lumen Trail backend API — SAAS-120 Lesson 2 starter.
//
// This file is the end-state of Lesson 1. It has four endpoints that Claude Code
// walked you through building: /health, /version, /echo (POST), /goodbye.
//
// In Lesson 2 you add real routes: /items (list), /items/:id (one), and POST /items
// with Zod validation on the request body.

import { Hono } from "hono";
import { serve } from "@hono/node-server";

const app = new Hono();

app.get("/health", (c) => {
  return c.json({ status: "ok" });
});

app.get("/version", (c) => {
  return c.json({
    name: "Lumen Trail API",
    version: "0.1.0",
    lesson: 2,
  });
});

app.get("/goodbye", (c) => {
  return c.json({ message: "See you on the trail!" });
});

app.post("/echo", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  return c.json({ youSent: body });
});

const port = Number(process.env.PORT ?? 3000);

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
  console.log(`Try: curl http://localhost:${info.port}/health`);
});
