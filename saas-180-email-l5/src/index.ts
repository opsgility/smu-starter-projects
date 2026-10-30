// Lumen Trail backend — SAAS-180 Lesson 5 starter.
//
// End state of Lesson 4 — Resend and MailHog transports are both wired, and
// a WelcomeEmail React Email component renders the welcome message. Lesson
// 5 is about lifecycle: welcome, password reset, invoice, and the anti-
// patterns that make legitimate email look like spam.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import nodemailer from "nodemailer";
import { Resend } from "resend";

const transport = nodemailer.createTransport({
  host: process.env.SMTP_HOST ?? "127.0.0.1",
  port: Number(process.env.SMTP_PORT ?? 1025),
  secure: false
});
const resend = new Resend(process.env.RESEND_API_KEY ?? "");
const EMAIL_PROVIDER = (process.env.EMAIL_PROVIDER ?? "mailhog") as "mailhog" | "resend";
const MAIL_FROM = process.env.MAIL_FROM ?? "Lumen Trail <no-reply@lumentrail.test>";

const app = new Hono();

app.get("/health", (c) =>
  c.json({ status: "ok", provider: EMAIL_PROVIDER })
);

async function sendMail(opts: {
  to: string;
  subject: string;
  html?: string;
  text: string;
}) {
  if (EMAIL_PROVIDER === "resend") {
    const res = await resend.emails.send({
      from: MAIL_FROM,
      to: opts.to,
      subject: opts.subject,
      text: opts.text,
      html: opts.html
    });
    return { messageId: res.data?.id ?? "unknown", provider: "resend" };
  }
  const info = await transport.sendMail({
    from: MAIL_FROM,
    to: opts.to,
    subject: opts.subject,
    text: opts.text,
    html: opts.html
  });
  return { messageId: info.messageId, provider: "mailhog" };
}

app.post("/signup", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const email = typeof body?.email === "string" ? body.email : "";
  if (!email) return c.json({ error: "email required" }, 400);
  await sendMail({
    to: email,
    subject: "Welcome to Lumen Trail",
    text: `Thanks for joining Lumen Trail. Start exploring routes at ${process.env.APP_BASE_URL ?? "https://lumentrail.test"}.`
  });
  return c.json({ ok: true });
});

app.post("/password-reset", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const email = typeof body?.email === "string" ? body.email : "";
  if (!email) return c.json({ error: "email required" }, 400);
  await sendMail({
    to: email,
    subject: "Reset your Lumen Trail password",
    text: `We received a request to reset your password. If this was not you, ignore this email.`
  });
  return c.json({ ok: true });
});

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
