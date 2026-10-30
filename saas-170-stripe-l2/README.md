# SAAS-170 Lesson 2 — Hosted Checkout for a one-time payment

Starter for the second lesson of **SAAS-170**. End state of Lesson 1 (Stripe account wired, Products + Prices created in the dashboard).

## Scenario

A user wants to buy a premium Lumen Trail route collection. In this lesson you add `POST /checkout` which creates a Stripe Checkout Session for the Product you created in the dashboard, then the frontend redirects the browser to Stripe's hosted Checkout page. Stripe runs the card form; your server never touches card numbers.

## Files

```
saas-170-stripe-l2/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health + /success + /cancel landing pages — Lesson 2 adds /checkout
```

## How to run

```
npm run dev
```

Open the Stripe dashboard side-by-side as you test — you will watch sessions appear under Payments → Checkout Sessions.

## Notes

- **Hosted Checkout** is the beginner-friendly path on Stripe. Stripe handles the card UI, 3-D Secure, and compliance — your API only creates sessions.
- **Elements and the Payment Element** are the alternative when you need Checkout inside your own UI. That is a Lesson 2 wrap-up pointer, not the main lesson.
