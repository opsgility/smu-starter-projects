// Lumen Trail backend — SAAS-180 Lesson 2 starter.
//
// End state of Lesson 1 (which was all mental model, no code). Lesson 2 adds
// POST /email/test which sends a plain-text message through MailHog using
// nodemailer. MailHog's SMTP server is running on 127.0.0.1:1025 and its
// UI is on http://localhost:8025. No inbox leaves the container.

import { Hono } from "hono";
import { serve } from "@hono/node-server";

const app = new Hono();

app.get("/health", (c) =>
  c.json({
    status: "ok",
    smtp: `${process.env.SMTP_HOST ?? "127.0.0.1"}:${process.env.SMTP_PORT ?? "1025"}`
  })
);

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
