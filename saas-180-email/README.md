# SAAS-180 Lesson 1 — The transactional-email mental model

Starter for the first lesson of **SAAS-180 — Transactional Email with MailHog and Resend** in the *SaaS Foundations with Claude Code* path. Lesson 1 is concept-only: From, Reply-To, SPF/DKIM/DMARC at the leader-explanation level, what makes mail land in Inbox vs Promotions vs Junk.

## Scenario

Lumen Trail sends four kinds of email: welcome, password reset, trip booking confirmation, monthly digest. These are **transactional** emails — triggered by a specific user action, high relevance, and the user wants them. Marketing email is a different world (compliance, unsubscribe, double opt-in) that is explicitly out of scope.

## Files

```
saas-180-email/
  README.md
  .gitignore
  .env.example           # SMTP_HOST + SMTP_PORT (MailHog) + RESEND_API_KEY placeholder
  package.json           # hono + nodemailer + resend + react-email (preinstalled)
  tsconfig.json
  src/index.ts           # bare /health — sends start in Lesson 2
```

## How to run

```
npm run dev
curl http://localhost:3000/health
```

## Notes

- **MailHog is already running** in the lab container (SMTP on `:1025`, UI on `:8025`). You open the UI by curling or by opening a tunneled browser tab per the lesson.
- **Resend is BYO account** — you grab a free API key in Lesson 3. The free tier easily covers the course.
