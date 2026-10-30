# SAAS-170 Lesson 1 — The Stripe object model

Starter for the first lesson of **SAAS-170 — Payments and Subscriptions with Stripe** in the *SaaS Foundations with Claude Code* path. Lesson 1 is about Stripe's object model, not Node code — you create a Product and a Price in the Stripe dashboard, run `stripe` CLI commands to inspect them, and sign in from the lab container.

## Scenario

Lumen Trail wants to charge for premium annotated route collections (one-time purchase) and a monthly "Pro" subscription. Stripe handles cards, 3-D Secure, tax, invoicing, and compliance for you — your API only ever creates Checkout Sessions and listens for webhook events.

## Pre-flight — the one external account

You bring your own free Stripe **test-mode** account:

1. Create an account at [https://dashboard.stripe.com/register](https://dashboard.stripe.com/register) (or sign in if you have one).
2. Make sure the dashboard's top banner says **Test mode**.
3. Grab a secret key from Developers → API keys. It starts with `sk_test_...`.
4. Paste into `.env` as `STRIPE_SECRET_KEY`.

Stripe is free in test mode — no card charged, nothing shipped.

## Files

```
saas-170-stripe/
  README.md
  .gitignore
  .env.example           # STRIPE_SECRET_KEY + STRIPE_PUBLISHABLE_KEY + webhook secret
  package.json           # hono + stripe (preinstalled in the lab container)
  tsconfig.json
  src/index.ts           # bare /health — code work starts in Lesson 2
```

## How to run

```
npm run dev
curl http://localhost:3000/health
```

`hasStripeKey` reflects whether your `.env` has `STRIPE_SECRET_KEY` set.

## Authentication

All Stripe API calls use your `sk_test_...` secret key. The **Stripe CLI** (`stripe` command, preinstalled in the SaaS stack container) is signed in with `stripe login` to the SAME account.

## Notes

- **This course never leaves test mode.** Every card number you can type in Checkout (4242 4242 4242 4242 for success, 4000 0000 0000 0002 for decline) is a Stripe test card.
- **No real money changes hands** — the dashboard shows every event, charge, and customer under "Test mode" and they do not sync to live mode.
