# SAAS-140 Lesson 2 — Cache-aside pattern

Starter for the second lesson of **SAAS-140 — Caching and Sessions with Redis**. This folder is the end state of Lesson 1 so you can start fresh.

## Scenario

Lumen Trail's homepage shows the five most popular routes. Behind the scenes that list is computed by a slow query — in production it joins routes, trips, and reviews, and in this starter it fakes the slow part with an 800ms delay. Every homepage visit pays that 800ms. The fix is **cache-aside**: look in Redis first; on a cache miss, run the slow computation and stash the result for a few minutes. In this lesson you add that pattern to the `/popular-routes` endpoint.

## Files

```
saas-140-redis-l2/
  README.md              # this file
  .gitignore             # Node ignores + .env
  .env.example           # REDIS_URL + PORT
  package.json           # Hono + ioredis + friends
  tsconfig.json          # Node 22 ESM + strict mode
  src/
    index.ts             # /health, /favorites/:userId (from Lesson 1), /popular-routes (slow, no cache)
```

## How to run

```
npm run dev
```

Hit the slow endpoint once (fresh terminal):

```
time curl http://localhost:3000/popular-routes
```

You'll see roughly 800ms of real time. By the end of this lesson a second call will come back in a few milliseconds.

## Authentication

None.

## Notes

- **Redis is already running on localhost:6379** — the container boots it as a managed sidecar. `redis-cli ping` returns `PONG`.
- **The `computePopularRoutes` function is intentionally slow** — don't optimize it. Caching is the lesson; the function stays as-is.
- **TTL matters.** You'll set a short expiration (60 seconds for this lesson) so stale data doesn't live forever. SAAS-220 covers how to measure whether your TTL is too long or too short.
