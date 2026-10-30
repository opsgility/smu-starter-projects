// Lumen Trail backend — SAAS-180 Lesson 1 starter.
//
// Lesson 1 is about the mental model (From/To/Reply-To, SPF/DKIM/DMARC at
// the leader-explanation level, deliverability basics). No sends yet.
// Lesson 2 adds the first MailHog send.

import { Hono } from "hono";
import { serve } from "@hono/node-server";

const app = new Hono();

app.get("/health", (c) =>
  c.json({
    status: "ok",
    smtp: `${process.env.SMTP_HOST ?? "127.0.0.1"}:${process.env.SMTP_PORT ?? "1025"}`,
    hasResendKey: !!process.env.RESEND_API_KEY
  })
);

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
