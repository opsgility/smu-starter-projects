// Lumen Trail backend — SAAS-170 Lesson 5 starter.
//
// End state of Lesson 4 — one-time Checkout, webhook listener, subscription
// Checkout, and /portal are all live. Lesson 5 hardens the webhook handler
// with idempotency so Stripe retries do not double-process events, and
// reconciles Stripe's view of a customer against a toy in-memory DB.

import { Hono } from "hono";
import { serve } from "@hono/node-server";
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY ?? "sk_test_PLACEHOLDER");
const APP_BASE_URL = process.env.APP_BASE_URL ?? "http://localhost:3000";
const WEBHOOK_SECRET = process.env.STRIPE_WEBHOOK_SECRET ?? "whsec_PLACEHOLDER";
const app = new Hono();

// Toy "database" — a real app persists in Postgres (SAAS-130) + Redis (SAAS-140).
const customers = new Map<string, { customerId: string; plan: "free" | "pro" }>();

app.get("/health", (c) =>
  c.json({ status: "ok", customers: customers.size })
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

app.post("/subscribe", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const priceId =
    typeof body?.priceId === "string"
      ? body.priceId
      : (process.env.STRIPE_SUB_PRICE_ID ?? "price_SUB_PLACEHOLDER");
  const session = await stripe.checkout.sessions.create({
    mode: "subscription",
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${APP_BASE_URL}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${APP_BASE_URL}/cancel`
  });
  return c.json({ sessionId: session.id, url: session.url });
});

app.post("/portal", async (c) => {
  const body = await c.req.json().catch(() => ({}));
  const customerId = typeof body?.customerId === "string" ? body.customerId : "";
  if (!customerId) return c.json({ error: "customerId required" }, 400);
  const session = await stripe.billingPortal.sessions.create({
    customer: customerId,
    return_url: APP_BASE_URL
  });
  return c.json({ url: session.url });
});

app.post("/webhooks/stripe", async (c) => {
  const sig = c.req.header("stripe-signature") ?? "";
  const buf = Buffer.from(await c.req.arrayBuffer());
  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(buf, sig, WEBHOOK_SECRET);
  } catch (err) {
    return c.json({ error: "signature invalid", detail: (err as Error).message }, 400);
  }
  // Lesson 5: wrap this switch in an idempotency guard so retries no-op.
  switch (event.type) {
    case "checkout.session.completed": {
      const s = event.data.object as Stripe.Checkout.Session;
      if (s.customer && s.mode === "subscription") {
        customers.set(String(s.customer), { customerId: String(s.customer), plan: "pro" });
        console.log(`[stripe] customer ${s.customer} is now pro`);
      }
      break;
    }
    case "customer.subscription.deleted": {
      const sub = event.data.object as Stripe.Subscription;
      customers.set(String(sub.customer), { customerId: String(sub.customer), plan: "free" });
      console.log(`[stripe] customer ${sub.customer} dropped to free`);
      break;
    }
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
