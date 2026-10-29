# SAAS-120 Lesson 4 — OpenAPI contracts + Swagger UI

Starter for the fourth lesson of **SAAS-120 — Backend APIs with Claude Code**. This folder is the end-state of Lesson 3 — structured error payloads, correct status codes, and idempotency keys are already in place.

## Scenario

**Lumen Trail**'s mobile team is ready to start calling the catalog API. They want a page they can open in a browser that lists every endpoint, shows what each one accepts and returns, and lets them try requests without a terminal. In Lesson 4 you give them that page — a Swagger UI docs site backed by an OpenAPI document — so your API becomes something they can read, not just hit.

## Files

```
saas-120-api-l4/
  README.md
  .env.example
  .gitignore
  package.json              # adds @hono/swagger-ui
  tsconfig.json
  src/
    index.ts                # /items with structured errors + Idempotency-Key
```

## How to run

```
npm run dev
```

Then in another terminal:

```
curl http://localhost:3000/items/does-not-exist
# {"error":{"code":"item_not_found","message":"No item with id 'does-not-exist'."}}

curl -i -X POST http://localhost:3000/items \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 2026-11-14-ski-sale-001" \
  -d '{"name":"Trail Mix","priceCents":799}'
# HTTP/1.1 201 Created
```

## Authentication

None — local only.

## Notes

- `@hono/swagger-ui` is added to the dependencies and is preinstalled in the ClaudeSaasStack container.
- The OpenAPI document in Lesson 4 is a hand-written JSON object — you don't need a schema generator. Claude Code teaches you the OpenAPI structure directly so you can read any API doc, not just this one.
