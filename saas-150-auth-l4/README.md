# SAAS-150 Lesson 4 — MFA (TOTP)

Starter for the fourth lesson of **SAAS-150**. This folder is the end-state of Lesson 3: password + OAuth + email verification + password reset, with single-use tokens hashed in the DB.

## Scenario

Lumen Trail now verifies email on signup and lets users reset their password. In Lesson 4 you add a second factor — TOTP (the Authenticator-app six-digit code) — so a stolen password alone isn't enough to take over an account.

## Files

```
saas-150-auth-l4/
  package.json                     # adds nodemailer
  migrations/
    0001_create_users.sql          # now with email_verified + github_user_id
    0002_create_sessions.sql
    0003_create_email_tokens.sql   # for verify + reset
  src/
    db.ts
    auth.ts                        # + newToken, hashToken (SHA-256-only in DB)
    mail.ts                        # nodemailer → MailHog on localhost:1025
    oauth.ts
    index.ts                       # + /verify-email, /password-reset/*
```

## How to run

```
cp .env.example .env
createdb lumentrail_auth
npm run migrate:up
npm run dev
```

Open `http://localhost:8025` in the preview browser to see MailHog's catch-all inbox. Every email the server sends lands there.

Try a signup:

```
curl -i -X POST http://localhost:3000/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"alex@lumentrail.example.com","display_name":"Alex","password":"super-secret"}'
```

Then open MailHog's UI and you'll see the verification email with a link like `http://localhost:3000/verify-email?token=...`. Click it (or curl it) to flip `email_verified` to true.

## Notes

- Tokens are 32 bytes of random base64url (~43 chars). Only the SHA-256 hash lands in the DB — if the DB leaks, the leaked rows aren't usable as tokens.
- Password reset invalidates every existing session for that user (so other devices get logged out).
- `/password-reset/request` always returns `{ ok: true }` even for unknown emails to avoid leaking which addresses are registered.
