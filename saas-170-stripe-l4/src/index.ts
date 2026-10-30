// Lumen Trail backend — SAAS-170 Lesson 4 starter.
//
// End state of Lesson 3 — /checkout creates sessions AND /webhooks/stripe
// receives signed events from the Stripe CLI. Lesson 4 adds subscriptions:
// POST /subscribe creates a recurring Checkout Session, and /portal opens
// Stripe's hosted customer portal so the user can upgrade, downgrade, or
// cancel.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? "sk_test_PLACEHOLDER");
const APP_BASE_URL = process.env.APP_BASE_URL ?? "http://localhost:3000";
const WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET ?? "whsec_PLACEHOLDER";
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

// Stripe sends raw body — Hono gives us arrayBuffer; keep that bytes-identical.
app.post("/webhooks/stripe", async (c) => {
  const sig = c.req.header("stripe-signature") ?? "";
  const buf = Buffer.from(await c.req.arrayBuffer());
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(buf, sig, WEBHOOK_SECRET);
  } catch (err) {
    return c.json({ error: "signature invalid", detail: (err as Error).message }, 400);
  }
  switch (event.type) {
    case "checkout.session.completed": {
      const s = event.data.object as Stripe.Checkout.Session;
      console.log(`[stripe] checkout completed — session ${s.id} customer ${s.customer}`);
      break;
    }
    case "invoice.paid":
      console.log(`[stripe] invoice paid`);
      break;
    default:
      console.log(`[stripe] unhandled event ${event.type}`);
  }
  return c.json({ received: true });
});

app.get("/success", (c) =>
  c.html(`<html><body><h1>Thanks for your purchase</h1></body></html>`)
);
app.get("/cancel", (c) => c.html(`<html><body><h1>Checkout cancelled</h1></body></html>`));

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
