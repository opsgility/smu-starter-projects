# SAAS-120 Lesson 5 — Testing with Claude Code

Starter for the fifth lesson of **SAAS-120 — Backend APIs with Claude Code**. This folder is the end-state of Lesson 4 — the API now serves `/openapi.json` and a Swagger UI page at `/docs`.

## Scenario

**Lumen Trail** is about to let the mobile team call the catalog API for real. Before that, you need confidence that changes don't silently break things. Lesson 5 teaches you how to direct Claude Code to write **tests** — the kind that catch regressions before customers do.

## Files

```
saas-120-api-l5/
  README.md
  .env.example
  .gitignore
  package.json              # adds vitest to devDependencies
  tsconfig.json
  vitest.config.ts          # scans tests/**/*.test.ts
  src/
    app.ts                  # Hono app — exported so tests can import it
    index.ts                # server entry point — opens a port
  tests/                    # empty — Claude Code fills it in during the lesson
    .gitkeep
```

## How to run

Start the server:

```
npm run dev
```

Open `http://localhost:3000/docs` for Swagger UI.

Run tests (Lesson 5 is where tests appear):

```
npm test
```

With no tests yet, vitest exits 0 after reporting zero test files, which is the expected starting state.

## Authentication

None — local only.

## Notes

- The server is split into `src/app.ts` (the Hono app, exported) and `src/index.ts` (the server start-up). Lesson 5's tests import `app` directly and call `app.request('/items')` — no port, no network, no process management.
- vitest is in devDependencies and preinstalled in the ClaudeSaasStack container.
