# SAAS-170 Lesson 3 — Webhooks and the Stripe CLI

Starter for the third lesson of **SAAS-170**. End state of Lesson 2 (Checkout Session creation working).

## Scenario

The user bought something. Your Checkout page said "success" and bounced them to /success. But **your server does not actually know they paid** — the browser can lie. The source of truth is Stripe, and Stripe tells you by firing a **webhook event** at a URL you register. In this lesson you add `/webhooks/stripe`, forward Stripe's events to it with `stripe listen --forward-to localhost:3000/webhooks/stripe`, and verify the signature so you only trust events that actually came from Stripe.

## Files

```
saas-170-stripe-l3/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health + /checkout + /success + /cancel
```

## How to run

Three terminals:

**Terminal 1 — the API:**
```
npm run dev
```

**Terminal 2 — Stripe webhook forwarder (sign in first with `stripe login`):**
```
stripe listen --forward-to localhost:3000/webhooks/stripe
```

The CLI prints a `whsec_...` secret — paste that as `STRIPE_WEBHOOK_SECRET` in `.env` and restart the API so it picks up the value.

**Terminal 3 — trigger a test event:**
```
stripe trigger checkout.session.completed
```

## Notes

- **Verifying the signature is mandatory.** Without it, anyone who can reach `/webhooks/stripe` can fake payment events. The `stripe.webhooks.constructEvent` call does the verification for you using the shared webhook secret.
- **Stripe retries webhooks** on 4xx/5xx responses for up to 3 days. Your handler must be idempotent — Lesson 5 adds that.
