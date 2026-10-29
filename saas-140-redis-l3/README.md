# SAAS-140 Lesson 3 — Redis-backed sessions

Starter for the third lesson of **SAAS-140 — Caching and Sessions with Redis**. End state of Lesson 2 so you can start fresh.

## Scenario

Lumen Trail users log in once at the start of a browsing session and expect to stay logged in while they jump between pages. In the starter, `POST /login` hands back a session id and the server remembers it in an **in-memory JavaScript `Map`**. That works for a demo but has two show-stopping problems:

1. **Restart the server and every user is logged out.** Users hate that.
2. **Spin up a second copy of the server behind a load balancer** (which every real SaaS does) and the two copies don't share session state. A user randomly logs out when their next request hits the other server.

The fix is to move the session store to Redis — one shared store that outlives any individual server process. This lesson walks you through that migration with Claude Code.

## Files

```
saas-140-redis-l3/
  README.md              # this file
  .gitignore             # Node ignores + .env
  .env.example           # REDIS_URL + PORT
  package.json           # Hono + ioredis + friends
  tsconfig.json          # Node 22 ESM + strict mode
  src/
    index.ts             # /health, /favorites, /popular-routes (cache-aside), /login, /me, /logout
```

## How to run

```
npm run dev
```

Try the broken-in-memory session flow:

```
curl -X POST http://localhost:3000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@lumentrail.test"}'
# → copy the sessionId from the response

curl http://localhost:3000/me -H "x-session-id: <paste-here>"
# → {"userId":"u-alice"}

# Now kill the dev server (Ctrl-C), restart it, and run /me again:
curl http://localhost:3000/me -H "x-session-id: <same-paste>"
# → 401 {"error":"no session"}
```

That logout-on-restart is the pain point. By the end of this lesson, the same curl works after a restart because the session lives in Redis.

## Authentication

The toy user "database" is a hardcoded object with two users. Real auth (hashing passwords, verifying them, OAuth, MFA) is covered end-to-end in **SAAS-150 — Authentication and User Identity**. This lesson stays focused on sessions.

## Notes

- **Why not JWTs?** Server-side sessions and JWTs are both valid patterns. Sessions are easier to invalidate (just delete the Redis key) and leak less data if a token is intercepted. SAAS-150 covers the tradeoffs.
- **TTL on sessions** — Redis will auto-expire session keys for you. You'll set a 7-day TTL in this lesson. That's the right default for a web app; a bank would use shorter.
