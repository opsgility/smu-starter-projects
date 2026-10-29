// Lumen Trail backend API — SAAS-140 Lesson 5 starter.
//
// End state of Lesson 4 — the POST /routes endpoint is rate-limited. This lesson
// introduces POST /signup, which registers a new user. Today signup does
// everything inline: create the user, send a welcome email, update analytics.
// Each of those is a side-effect that we don't want blocking the HTTP response.
// Your job is to refactor signup so it just creates the user, then publishes a
// "user-signed-up" event on Redis pub/sub. A separate worker process (src/worker.ts)
// subscribes to that channel and does the slow follow-up work. If the worker is
// down, signup still succeeds.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { randomUUID } from "node:crypto";
import Redis from "ioredis";

const redis = new Redis(process.env.REDIS_URL ?? "redis://127.0.0.1:6379");
const app = new Hono();

app.get("/health", (c) => c.json({ status: "ok" }));

// ---- Everything from Lessons 1-4 is still here ----
// (favorites, popular routes with cache-aside, Redis-backed sessions, rate-limited /routes)
// Omitted from this excerpt for brevity — Claude Code can show you the whole file
// at any time. The focus of this lesson is signup.

// ---- NEW: signup with inline side effects ----

const userStore: Array<{ id: string; email: string; createdAt: number }> = [];

async function sendWelcomeEmail(email: string) {
  // Fake "slow email send". In SAAS-180 you plug in real transactional email.
  await new Promise((r) => setTimeout(r, 500));
  console.log(`[inline] welcome email sent to ${email}`);
}

async function recordAnalyticsSignup(userId: string) {
  // Fake "slow analytics write".
  await new Promise((r) => setTimeout(r, 300));
  console.log(`[inline] analytics recorded signup for ${userId}`);
}

app.post("/signup", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const email = typeof body?.email === "string" ? body.email : "";
  if (!email) return c.json({ error: "email required" }, 400);

  const user = { id: `u-${randomUUID().slice(0, 8)}`, email, createdAt: Date.now() };
  userStore.push(user);

  // The problem: these two awaits block the HTTP response for ~800ms.
  // If recordAnalyticsSignup throws, the user never gets the email either.
  await sendWelcomeEmail(email);
  await recordAnalyticsSignup(user.id);

  return c.json(user, 201);
});

const port = Number(process.env.PORT ?? 3000);

serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
