# SAAS-180 Lesson 5 — Lifecycle emails and anti-patterns

Starter for the fifth and final lesson of **SAAS-180**. End state of Lesson 4 (React Email templates working).

## Scenario

With the plumbing solved, it is time to actually ship the four Lumen Trail transactional emails: welcome (on signup), password reset (on request), trip booking confirmation (on payment success — ties into SAAS-170), and monthly digest (optional, from a scheduled worker — ties into SAAS-190). Then: the anti-patterns that cause legitimate email to end up in Promotions or Junk.

## Files

```
saas-180-email-l5/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health + /email/test + /signup + /password-reset
```

## How to run

```
npm run dev
```

Trigger each lifecycle email with curl and inspect the output in MailHog or your Resend inbox.

## Notes

- **The anti-patterns that get you flagged as spam** — image-only mail, misleading subject lines, missing Reply-To, missing plain-text alternative, cold recipients. The lesson covers each.
- **End of SAAS-180.** You can send well-shaped transactional email from your SaaS, locally for dev and via Resend for prod, with React-based templates and lifecycle discipline.
