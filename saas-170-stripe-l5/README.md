# SAAS-170 Lesson 5 — Idempotency, retries, and reconciliation

Starter for the fifth and final lesson of **SAAS-170**. End state of Lesson 4 (subscriptions and portal working).

## Scenario

Stripe retries webhooks aggressively — up to 3 days with exponential backoff — because the alternative (losing an event) is unacceptable. That means **your webhook handler will be called more than once for the same event** in production, and your logic must tolerate that. Lesson 5 adds idempotency to the webhook, then shows how to reconcile Stripe's view of a customer against your own database so a dropped webhook does not leave you out of sync.

## Files

```
saas-170-stripe-l5/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health + /checkout + /subscribe + /portal + /webhooks/stripe + /success + /cancel
```

## How to run

Same three-terminal setup as prior lessons. Use `stripe trigger` to replay events and watch your idempotency guard do its job.

## Notes

- **Idempotency key** = Stripe's `event.id`. Store the id in Redis (SAAS-140 territory) or Postgres (SAAS-130) with a short TTL; on each incoming event, SETNX / INSERT-IGNORE first, and if the key already existed, no-op.
- **Reconciliation** = the quiet background check that your DB matches Stripe. Weekly cron that lists all active subscriptions in Stripe, compares against your DB, flags discrepancies.
- **End of SAAS-170.** Payments, subscriptions, portal, webhooks, idempotency. The full beginner stack.
