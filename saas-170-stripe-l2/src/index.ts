// Lumen Trail backend — SAAS-170 Lesson 2 starter.
//
// End state of Lesson 1 — Stripe is wired up but there is no endpoint yet.
// Lesson 2 adds POST /checkout which creates a Stripe Checkout Session for
// a one-time premium-collection purchase, plus a /success and /cancel
// landing page the Checkout returns to.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? "sk_test_PLACEHOLDER");
const APP_BASE_URL = process.env.APP_BASE_URL ?? "http://localhost:3000";
const app = new Hono();

app.get("/health", (c) =>
  c.json({ status: "ok", hasStripeKey: !!process.env.STRIPE_SECRET_KEY })
);

app.get("/success", (c) =>
  c.html(
    `<html><body style="font-family: system-ui; max-width: 480px; margin: 60px auto">
       <h1>Thanks for your purchase</h1>
       <p>Session: ${c.req.query("session_id") ?? "<missing>"}</p>
       <p><a href="/">Back to Lumen Trail</a></p>
     </body></html>`
  )
);

app.get("/cancel", (c) =>
  c.html(
    `<html><body style="font-family: system-ui; max-width: 480px; margin: 60px auto">
       <h1>Checkout cancelled</h1>
       <p>You were not charged. <a href="/">Back to Lumen Trail</a>.</p>
     </body></html>`
  )
);

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
