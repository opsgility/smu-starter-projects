// Lumen Trail backend — SAAS-170 Lesson 3 starter.
//
// End state of Lesson 2 — POST /checkout creates a one-time Checkout Session
// and the user lands back on /success or /cancel. Lesson 3 adds the webhook
// listener so your API finds out when a payment actually succeeded.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? "sk_test_PLACEHOLDER");
const APP_BASE_URL = process.env.APP_BASE_URL ?? "http://localhost:3000";
const app = new Hono();

app.get("/health", (c) =>
  c.json({ status: "ok", hasStripeKey: !!process.env.STRIPE_SECRET_KEY })
);

app.post("/checkout", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const priceId =
    typeof body?.priceId === "string"
      ? body.priceId
      : (process.env.STRIPE_PRICE_ID ?? "price_PLACEHOLDER");
  const session = await stripe.checkout.sessions.create({
    mode: "payment",
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${APP_BASE_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${APP_BASE_URL}/cancel`
  });
  return c.json({ sessionId: session.id, url: session.url });
});

app.get("/success", (c) =>
  c.html(
    `<html><body style="font-family: system-ui; max-width: 480px; margin: 60px auto">
       <h1>Thanks for your purchase</h1>
       <p>Session: ${c.req.query("session_id") ?? "<missing>"}</p>
     </body></html>`
  )
);

app.get("/cancel", (c) =>
  c.html(`<html><body><h1>Checkout cancelled</h1></body></html>`)
);

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
