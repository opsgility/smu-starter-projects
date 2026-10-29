# SAAS-150 Lesson 2 — OAuth2 sign-in

Starter for the second lesson of **SAAS-150 — Authentication and User Identity**. This folder is the end-state of Lesson 1: password hashing + session cookies + four working auth endpoints.

## Scenario

Lumen Trail now lets customers sign up with email + password. In Lesson 2 you add a second way to sign in: **"Sign in with GitHub"**, so new users can create an account without typing a password.

## Files

```
saas-150-auth-l2/
  README.md
  .env.example
  .gitignore
  package.json              # adds argon2
  tsconfig.json
  .pgmigraterc.json
  migrations/
    0001_create_users.sql
    0002_create_sessions.sql
  src/
    db.ts
    auth.ts                 # hashPassword, verifyPassword, createSession, requireUser
    index.ts                # /signup, /signin, /signout, /me all working
```

## How to run

```
cp .env.example .env
createdb lumentrail_auth
npm run migrate:up
npm run dev
```

Then exercise it:

```
curl -i -X POST http://localhost:3000/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"alex@lumentrail.example.com","display_name":"Alex","password":"super-secret"}'
# HTTP/1.1 201 Created + Set-Cookie: lt_session=...

curl -b "lt_session=..." http://localhost:3000/me
# { "id": 1, "email": "alex@...", "display_name": "Alex" }
```

## Notes

- Passwords are hashed with Argon2id defaults (`argon2` npm package).
- Session cookie is `lt_session`, HttpOnly + SameSite=Lax, 30-day TTL.
- Signin uses a dummy hash on nonexistent emails so timing doesn't leak which emails are registered.
