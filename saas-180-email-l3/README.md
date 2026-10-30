# SAAS-180 Lesson 3 — Resend for real sends

Starter for the third lesson of **SAAS-180**. End state of Lesson 2 (MailHog send working).

## Scenario

MailHog is for development. Production needs a real email provider. **Resend** is a modern developer-first platform with a generous free tier, a clean Node SDK, and sensible defaults. In this lesson you create a Resend account, verify a sender address on their `onboarding@resend.dev` domain, and swap the API's transport from MailHog to Resend for real sends — toggled by one env var.

## Pre-flight — the one external account

1. Sign up for free at [https://resend.com](https://resend.com).
2. Grab an API key from the dashboard — it starts with `re_`.
3. Paste it as `RESEND_API_KEY` in `.env`.
4. By default Resend lets you send FROM `onboarding@resend.dev` TO the email you signed up with — perfect for testing.

Everything stays on the free tier.

## Files

```
saas-180-email-l3/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health + POST /email/test (MailHog via nodemailer, from L2)
```

## How to run

```
npm run dev
```

Then set `EMAIL_PROVIDER=resend` in `.env` to flip the transport.

## Notes

- **The flip is one env var** — no code changes between dev and prod transports.
- **Deliverability — SPF, DKIM, DMARC** — Resend handles the technical bits for you. For your own domain you add three DNS records and Resend verifies them. The lesson walks through the records at the concept level.
