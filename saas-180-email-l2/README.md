# SAAS-180 Lesson 2 — Local-only with MailHog

Starter for the second lesson of **SAAS-180**. End state of Lesson 1 (concept-only).

## Scenario

The tightest feedback loop for email is a local SMTP server that intercepts every outgoing message and displays it in a browser UI — no real inbox, no external account, no deliverability variance. That is MailHog. In this lesson you add `POST /email/test` that sends a message through MailHog via nodemailer and verify it in the UI.

## Files

```
saas-180-email-l2/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health only — Lesson 2 adds POST /email/test
```

## How to run

```
npm run dev
```

Then open the MailHog UI in a browser tab pointed at `http://localhost:8025` (the lab exposes port 8025).

## Notes

- **nodemailer** is the de-facto Node SMTP client. It can target any SMTP server — MailHog in dev, Resend's SMTP endpoint if you ever need it in prod, your corporate SMTP relay, etc.
- **MailHog never actually sends** — it just captures. So you can run `/email/test` a thousand times without worrying about rate limits, reputation, or recipients.
