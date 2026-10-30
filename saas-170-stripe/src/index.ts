// Lumen Trail backend — SAAS-170 Lesson 1 starter.
//
// Lesson 1 is about the Stripe object model (Products, Prices, Checkout
// Sessions, Customers) — most of the lesson happens in the Stripe dashboard
// and in `stripe` CLI calls, not here. By the end of Lesson 2 this file has
// a /checkout endpoint that creates a Checkout Session.

import { Hono } from "hono";
import { serve } from "@hono/node-server";

const app = new Hono();

app.get("/health", (c) =>
  c.json({
    status: "ok",
    hasStripeKey: !!process.env.STRIPE_SECRET_KEY
  })
);

const port = Number(process.env.PORT ?? 3000);
serve({ fetch: app.fetch, port }, (info) => {
  console.log(`Lumen Trail API listening on http://localhost:${info.port}`);
});
