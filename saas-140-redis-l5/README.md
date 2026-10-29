# SAAS-140 Lesson 5 — Pub/sub for lightweight events

Starter for the fifth and final lesson of **SAAS-140 — Caching and Sessions with Redis**. End state of Lesson 4 so you can start fresh.

## Scenario

A user signs up. In today's code the signup handler does three things in a row:

1. Store the user.
2. Send a welcome email (fake 500ms in this starter; SAAS-180 teaches real sends).
3. Record a signup event in analytics (fake 300ms).

That means the HTTP response takes about 800ms, and if step 3 throws, the user never gets their email. Both are symptoms of **doing follow-up work inline**. The fix is **pub/sub**: the signup handler stores the user, publishes a `user-signed-up` event on a Redis channel, and returns to the client right away. A separate **worker process** subscribes to that channel and does the slow follow-up. If the worker is down, signup still succeeds — the event just queues up until the worker comes back (and in a production system you'd upgrade to Redis Streams for guaranteed delivery; this lesson teaches basic pub/sub first).

## Files

```
saas-140-redis-l5/
  README.md              # this file
  .gitignore             # Node ignores + .env
  .env.example           # REDIS_URL + PORT
  package.json           # Hono + ioredis + friends; adds a `worker` script
  tsconfig.json          # Node 22 ESM + strict mode
  src/
    index.ts             # API — POST /signup does everything inline (the problem)
    worker.ts            # the second process you'll grow — currently just prints "connected"
```

## How to run

Two terminals this time:

**Terminal 1 — the API:**
```
npm run dev
```

**Terminal 2 — the worker:**
```
npm run worker
```

**Terminal 3 — hit signup:**
```
time curl -X POST http://localhost:3000/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"carol@lumentrail.test"}'
```

Today you'll see ~800ms. By the end of this lesson, signup returns in under 20ms and the worker's terminal prints the "sent welcome email" and "recorded analytics" lines a moment later.

## Notes

- **Pub/sub vs streams.** Redis pub/sub is fire-and-forget — if no subscriber is listening, the message is lost. Redis Streams add guaranteed delivery and consumer groups. For truly critical events (payments, order state), use Streams; for welcome emails and analytics, pub/sub is fine. SAAS-190 goes further with job queues (BullMQ) when you need retries, scheduling, and dead-letter handling.
- **The signup is still synchronous w.r.t. storing the user** — that must happen before the response so the client gets a user id back. Only the follow-up effects move off the critical path.
- **Two processes.** This is your first course that runs more than one Node process at once. It's also what a real SaaS deployment looks like — an API server and one or more worker servers, both talking to the same Redis.
