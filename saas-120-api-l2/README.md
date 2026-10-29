# SAAS-120 Lesson 2 — Routing, request validation, response shaping

Starter for the second lesson of **SAAS-120 — Backend APIs with Claude Code**. This folder is the end-state of Lesson 1 so you can start fresh without re-building the four endpoints from the first lesson.

## Scenario

You are building the backend API for **Lumen Trail**, a fictional company that rents camping gear and sells trail-food subscriptions. Lesson 1 got the service running with a health check and a few toy endpoints. Lesson 2 is where you add the first real resource: `items` (the gear catalog).

## Files

```
saas-120-api-l2/
  README.md                 # this file
  .env.example              # PORT only — copy to .env if you want to change ports
  .gitignore                # Node ignores + .env
  package.json              # hono, @hono/node-server, zod — all preinstalled in the lab container
  tsconfig.json             # Node 22 ESM + strict mode
  src/
    index.ts                # the API — four endpoints from Lesson 1 are already here
```

## How to run

In the integrated VS Code terminal:

```
npm run dev
```

That starts the server on `http://localhost:3000`. In a second terminal:

```
curl http://localhost:3000/health
```

Response: `{"status":"ok"}`.

## Authentication

None. This is a local service on `localhost` only — nothing is exposed to the internet.

## Notes

- Zod is already listed as a dependency and installed in the ClaudeSaasStack container — Claude Code will import it as `import { z } from "zod"` in Lesson 2's exercises.
- `tsx watch` auto-reloads the server when files change in `src/`. You should not need to stop and restart it.
- If a port is already in use, change `PORT` in `.env` (copy from `.env.example`).
