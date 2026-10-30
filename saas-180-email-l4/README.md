# SAAS-180 Lesson 4 — Templates with React Email

Starter for the fourth lesson of **SAAS-180**. End state of Lesson 3 (Resend transport working).

## Scenario

Hand-rolled HTML strings for email are miserable — tables for layout, inline styles, 15-year-old client quirks. **React Email** lets you author templates as React components, render them to Email-safe HTML, and get decent-looking email in Gmail, Outlook, and Apple Mail without becoming an expert on `<mso-conditional>` tags.

## Files

```
saas-180-email-l4/
  README.md
  .gitignore
  .env.example
  package.json
  tsconfig.json
  src/index.ts           # /health + /email/test with EMAIL_PROVIDER switch (from L3)
```

## How to run

```
npm run dev
```

In this lesson you add `src/emails/WelcomeEmail.tsx`, render it with `render(<WelcomeEmail name="Alice" />)` from `@react-email/components`, and pass the resulting HTML to the transport.

## Notes

- **Component-based templates** can be previewed in a browser via `npx react-email dev` while you iterate.
- **Shared design** — the same components can underlie your frontend's styled transactional pages (the magic-link confirmation page, etc.) in SAAS-250.
