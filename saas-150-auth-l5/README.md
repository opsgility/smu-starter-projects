# SAAS-150 Lesson 5 — Roles + authorization

Starter for the fifth and final lesson of **SAAS-150**. This folder is the end-state of Lesson 4: password + OAuth + email verification + password reset + TOTP MFA with backup codes.

## Scenario

Lumen Trail users can sign up, verify, log in, reset, and protect their account with 2FA. In Lesson 5 you add **authorization**: a `role` column (user / admin) on the users table, a route-level middleware, and ownership checks on resource endpoints — so admins get special access and regular users can only touch their own data.

## Files

```
saas-150-auth-l5/
  package.json              # adds otplib, qrcode
  migrations/
    0001_create_users.sql           # + totp_secret, totp_enabled
    0002_create_sessions.sql
    0003_create_email_tokens.sql
    0004_create_mfa_challenges.sql  # intermediate "password OK, now prove MFA"
    0005_create_backup_codes.sql    # hashed one-time recovery codes
  src/
    db.ts
    auth.ts                 # session + password + token helpers
    mfa.ts                  # TOTP generate / verify, backup codes
    mail.ts
    oauth.ts
    index.ts                # all endpoints — password + OAuth + email + MFA
```

## Signin flow with MFA

```
POST /signin  { email, password }
  if user.totp_enabled is false:
    -> 200 { id, email, display_name }  (session cookie set)
  if user.totp_enabled is true:
    -> 200 { requires_mfa: true, mfa_token: "..." }
POST /signin/verify-totp  { mfa_token, code }
  if code matches TOTP or an unused backup code:
    -> 200 { id, email, display_name }  (session cookie set)
```

## How to run

```
cp .env.example .env
createdb lumentrail_auth
npm run migrate:up
npm run dev
```

Enroll your Authenticator app:

```
# Sign in first (as before).
curl -b "lt_session=..." -X POST http://localhost:3000/mfa/enroll/start
# Response has `qr_code` as a data: URL — paste into a browser or save to a file to scan.
```

Scan the QR with your phone's Authenticator app, then confirm:

```
curl -b "lt_session=..." -X POST http://localhost:3000/mfa/enroll/verify \
  -H "Content-Type: application/json" \
  -d '{"code":"123456"}'
# Response includes 10 one-time backup codes — store them.
```

## Notes

- `totp_secret` is stored in plaintext in this lab for simplicity. In production, encrypt-at-rest with a KMS key (`pgcrypto`, Azure Key Vault, or GCP Cloud KMS).
- Backup codes are stored as Argon2id hashes — same discipline as passwords.
- MFA challenges expire after 10 minutes to prevent a stolen `mfa_token` from being replayed hours later.
