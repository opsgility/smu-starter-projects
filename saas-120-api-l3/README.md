# SAAS-120 Lesson 3 — Error handling, status codes, idempotency

Starter for the third lesson of **SAAS-120 — Backend APIs with Claude Code**. This folder is the end-state of Lesson 2 — the `/items` resource is already here with Zod validation, which gives Lesson 3 something to improve.

## Scenario

**Lumen Trail** needs its API to behave properly when things go wrong. Right now, a missing item returns a vague `"not found"` string. A bad request body returns a Zod blob the mobile team can't easily parse. And if the "create order" button double-fires on a flaky connection, Lumen Trail creates two items instead of one. Lesson 3 fixes all of that.

## Files

```
saas-120-api-l3/
  README.md
  .env.example
  .gitignore
  package.json
  tsconfig.json
  src/
    index.ts                # /items CRUD with Zod validation, from Lesson 2
```

## How to run

```
npm run dev
```

Then in another terminal:

```
curl http://localhost:3000/items
curl -X POST http://localhost:3000/items -H "Content-Type: application/json" -d '{"name":"Trail Mix","priceCents":799}'
```

## Authentication

None — local only.

## Notes

- All packages (hono, zod, @hono/node-server, tsx) are preinstalled in the ClaudeSaasStack lab container. You never run `npm install`.
- The in-memory `items` Map is cleared every time you restart the server. That is intentional for the lab — a real service would use Postgres (which SAAS-130 covers).
