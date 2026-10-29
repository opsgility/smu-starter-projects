# SAAS-140 Lesson 4 — Rate limiting with Redis

Starter for the fourth lesson of **SAAS-140 — Caching and Sessions with Redis**. End state of Lesson 3 (sessions in Redis) so you can start fresh.

## Scenario

Lumen Trail now accepts user-submitted routes. The `POST /routes` endpoint takes a name, assigns an id, and stashes it. In the real product this is a juicy target for abuse — a single angry user with a script can call this endpoint in a tight loop and flood the catalog with junk. In this lesson you add **rate limiting**: a per-IP counter and a per-user counter stored in Redis. If a caller exceeds a threshold inside a one-minute window, the API returns `429 Too Many Requests` with a `Retry-After` header instead of running the handler.

Rate limiting has two popular shapes:

- **Fixed-window** — one counter per IP per minute. Simple. Edge-of-the-window traffic can double the effective rate.
- **Sliding-window** — a sorted set of request timestamps per IP. More accurate; slightly more Redis work.

You'll implement both in this lesson so you understand the tradeoff.

## Files

```
saas-140-redis-l4/
  README.md              # this file
  .gitignore             # Node ignores + .env
  .env.example           # REDIS_URL + PORT
  package.json           # Hono + ioredis + friends
  tsconfig.json          # Node 22 ESM + strict mode
  src/
    index.ts             # everything from L1-L3 plus POST /routes (unprotected)
```

## How to run

```
npm run dev
```

Hammer the unprotected endpoint from a second terminal:

```
for i in $(seq 1 20); do
  curl -sX POST http://localhost:3000/routes \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"junk-$i\"}" | head -c 80
  echo
done
```

Twenty routes landed with no pushback — that's the problem. By the end of this lesson the same loop stops after a handful of calls and returns `429` for the rest.

## Notes

- **The lesson teaches the Redis primitives**, not a library. There's a Hono rate-limit plugin that would do all this for you, but the point here is understanding what the plugin does under the hood so you can tune or replace it later. **SAAS-240 — Rate Limiting and API Protection** goes deeper and does bring in the Hono middleware + Nginx reverse-proxy pattern.
- **Why Redis and not an in-memory counter?** The in-memory counter resets on restart and doesn't aggregate across multiple server instances behind a load balancer. Both failure modes let a determined attacker through. The same reason sessions moved to Redis in Lesson 3.
