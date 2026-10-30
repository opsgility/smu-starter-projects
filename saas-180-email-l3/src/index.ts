// Lumen Trail backend — SAAS-180 Lesson 3 starter.
//
// End state of Lesson 2 — POST /email/test sends through MailHog via
// nodemailer. Everything is captured in MailHog's UI at :8025. Lesson 3
// swaps the transport to Resend for real sends to a verified test inbox.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import nodemailer from "nodemailer";

const transport = nodemailer.createTransport({
  host: process.env.SMTP_HOST ?? "127.0.0.1",
  port: Number(process.env.SMTP_PORT ?? 1025),
  secure: false
});
const MAIL_FROM = process.env.MAIL_FROM ?? "Lumen Trail <no-reply@lumentrail.test>";

const app = new Hono();

app.get("/health", (c) =>
  c.json({ status: "ok", transport: "nodemailer-mailhog" })
);

app.post("/email/test", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const to = typeof body?.to === "string" ? body.to : "test@lumentrail.test";
  const subject =
    typeof body?.subject === "string" ? body.subject : "Hello from Lumen Trail";
  const text =
    typeof body?.text === "string" ? body.text : "This is a test message.";

  const info = await transport.sendMail({ from: MAIL_FROM, to, subject, text });
  return c.json({ messageId: info.messageId, accepted: info.accepted });
});

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
