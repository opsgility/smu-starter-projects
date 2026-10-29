# SAAS-150 Lesson 1 — Auth scaffold

Starter for the first lesson of **SAAS-150 — Authentication and User Identity**. This folder is a minimal Hono API with a Postgres connection and migrations for `users` + `sessions`. The four auth endpoints (`/signup`, `/signin`, `/signout`, `/me`) are stubbed with 501 responses — Lesson 1 fills them in.

## Scenario

**Lumen Trail** — the camping-gear subscription business — now needs real customer accounts. In SAAS-130 you had a `users` table with just email and display_name. In SAAS-150 you give those users passwords, OAuth sign-in, email verification, MFA, and roles.

## Files

```
saas-150-auth/
  README.md
  .env.example                      # DATABASE_URL + SESSION_SECRET
  .gitignore
  package.json                      # hono, pg, zod, node-pg-migrate
  tsconfig.json
  .pgmigraterc.json                 # node-pg-migrate config
  migrations/
    0001_create_users.sql           # id, email UNIQUE, display_name, password_hash (nullable), created_at
    0002_create_sessions.sql        # id, user_id FK, expires_at, created_at + index on user_id
  src/
    db.ts                           # shared pg Pool
    index.ts                        # Hono app with four stubbed auth endpoints
```

## How to run

```
cp .env.example .env
createdb lumentrail_auth
npm run migrate:up
npm run dev
```

Server listens on `http://localhost:3000`. Hit the stubs:

```
curl -i -X POST http://localhost:3000/signup
# HTTP 501 { "error": "not implemented yet — Lesson 1 fills this in" }
```

## Authentication

Local only. The container's Postgres uses `postgres`/`postgres`. No real credentials needed yet.

## Notes

- `password_hash` is nullable so you can create OAuth-only users (Lesson 2) without a password.
- The `sessions` table uses TEXT primary keys so session ids can be opaque random strings, not sequential integers.
- `ON DELETE CASCADE` on `sessions.user_id` deletes a user's sessions when the user is deleted.
