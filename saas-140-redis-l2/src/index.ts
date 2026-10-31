// Lumen Trail backend API — SAAS-140 Lesson 2 starter.
//
// Minimal scaffold. SAAS-140 is a Claude-Code-driven course: the student
// directs Claude Code to add Redis caching / sessions / rate limiting /
// pub+sub to this file across the lesson's exercises. Starts from almost
// nothing — the exercises walk the full build.
//
// Open the exercises in the right pane of the lab for step-by-step
// directives to paste into Claude Code.

import { Hono } from "hono";
import { serve } from "@hono/node-server";

const app = new Hono();

app.get("/health", (c) => c.json({ status: "ok" }));

const port = Number(process.env.PORT ?? 3000);

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
