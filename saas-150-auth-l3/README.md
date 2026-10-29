# SAAS-150 Lesson 3 — Email verification + password reset

Starter for the third lesson of **SAAS-150**. This folder is the end-state of Lesson 2: password-based auth PLUS GitHub OAuth.

## Scenario

Lumen Trail now supports two sign-in paths: email + password, and "Sign in with GitHub." In Lesson 3 you add the single-use-token pattern — email verification on sign-up, password reset on request.

## Files

```
saas-150-auth-l3/
  package.json                 # adds arctic (OAuth)
  migrations/
    0001_create_users.sql
    0002_create_sessions.sql
    0003_add_github_user_id.sql
  src/
    db.ts
    auth.ts                    # same session + password helpers from L1
    oauth.ts                   # arctic GitHub client
    index.ts                   # + /oauth/github/start, /oauth/github/callback
```

## How to run

```
cp .env.example .env
# Fill in GITHUB_CLIENT_ID + GITHUB_CLIENT_SECRET from your GitHub OAuth app
createdb lumentrail_auth
npm run migrate:up
npm run dev
```

Open `http://localhost:3000/oauth/github/start` in a browser — you'll be redirected to GitHub, approve, and redirected back to `/me` with a session cookie.

## Notes

- OAuth state is stored in a short-lived cookie to prevent CSRF on the callback.
- GitHub's `/user` endpoint may not return email; we fall back to `/user/emails`.
- If a GitHub profile's email matches an existing password user, the two accounts are linked (same `users` row, now with `github_user_id` set).
