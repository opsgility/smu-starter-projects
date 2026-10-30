# SAAS-170 Lesson 4 — Subscriptions and the customer portal

Starter for the fourth lesson of **SAAS-170**. End state of Lesson 3 (webhooks wired and verified).

## Scenario

Lumen Trail wants a monthly "Pro" plan. In this lesson you create a recurring Price in the dashboard, add `POST /subscribe` that creates a subscription-mode Checkout Session, listen for the `customer.subscription.created` and `.deleted` webhook events, and add `POST /portal` which hands the user a one-time URL to Stripe's hosted **customer portal** for upgrading, downgrading, or cancelling.

## Files

```
saas-170-stripe-l4/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health + /checkout (one-time) + /webhooks/stripe + /success + /cancel
```

## How to run

Same three-terminal setup as Lesson 3 — API, `stripe listen`, and curl. Test subscription Checkout with card `4242 4242 4242 4242`.

## Notes

- **The portal does the heavy lifting.** You do not need to build upgrade / downgrade / cancel UIs — Stripe runs them, you just link to the portal URL.
- **Metered billing, trials, discounts, and tax** are all portal-configurable at the Product + Price level in the dashboard. The code in your API barely changes.
