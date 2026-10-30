// Lumen Trail backend — SAAS-180 Lesson 4 starter.
//
// End state of Lesson 3 — the transport can be switched between MailHog
// and Resend via EMAIL_PROVIDER. Lesson 4 adds React Email components so
// your templates live in the same codebase as your frontend.

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

async function sendMail(opts: { to: string; subject: string; text: string }) {
  if (EMAIL_PROVIDER === "resend") {
    const res = await resend.emails.send({
      from: MAIL_FROM,
      to: opts.to,
      subject: opts.subject,
      text: opts.text
    });
    return { messageId: res.data?.id ?? "unknown", provider: "resend" };
  }
  const info = await transport.sendMail({
    from: MAIL_FROM,
    to: opts.to,
    subject: opts.subject,
    text: opts.text
  });
  return { messageId: info.messageId, provider: "mailhog" };
}

app.post("/email/test", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const to = typeof body?.to === "string" ? body.to : "test@lumentrail.test";
  const subject =
    typeof body?.subject === "string" ? body.subject : "Hello from Lumen Trail";
  const text =
    typeof body?.text === "string" ? body.text : "This is a test message.";
  const result = await sendMail({ to, subject, text });
  return c.json(result);
});

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
