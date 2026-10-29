# SAAS-140 Lesson 1 — What Redis is and the kv data model

Starter for the first lesson of **SAAS-140 — Caching and Sessions with Redis** in the *SaaS Foundations with Claude Code* path. This folder is almost empty on purpose. Lesson 1 is where you learn Redis itself — what a key-value store is, which data types it supports, and how a Node app talks to it — before any of the real SaaS patterns in the later lessons.

## Scenario

**Lumen Trail** is a hiking-route marketplace. Users browse routes, favorite the ones they want to come back to, and buy premium annotated collections. The frontend hits a Node API; the API reads and writes to a PostgreSQL database. That already works — but every page load re-queries Postgres for things that don't change often, logins are stored in server memory and die when the server restarts, and a single abusive user can hammer the create-route endpoint without any throttling. Redis is the missing piece. In this lesson you meet the tool itself; the next four lessons apply it to those real problems.

## Files

```
saas-140-redis/
  README.md              # this file
  .gitignore             # Node ignores + .env
  .env.example           # REDIS_URL + PORT
  package.json           # Hono + @hono/node-server + ioredis — all preinstalled in the container
  tsconfig.json          # Node 22 ESM + strict mode
  src/
    index.ts             # the API — one /health endpoint, nothing else
```

## How to run

The SkillMeUp lab container opens this folder in VS Code when the lab starts. **Redis 7 is already running** in the container on `localhost:6379`. Node 22, Claude Code, and all the npm packages are preinstalled. You do NOT need to run `npm install` or start Redis — the environment did both for you.

Start the API in dev mode (reloads on file save):

```
npm run dev
```

Confirm Redis is alive from a second terminal:

```
redis-cli ping
```

That should print `PONG`.

Then confirm the API:

```
curl http://localhost:3000/health
```

That should print `{"status":"ok"}`.

To use Claude Code as your coding partner:

```
claude
```

Every lesson of SAAS-140 asks you to drive Claude Code through the Redis changes rather than typing the code yourself. The point of this course is learning to direct the AI, not learning TypeScript syntax.

## Authentication

None. SAAS-140 is local to the lab container. The Redis instance is unauthenticated and listens only on localhost — exactly what a dev environment should look like. SAAS-230 covers how to swap this out for a managed Redis with real auth when you ship to production.

## Notes

- **Redis is already running** — you don't need `redis-server` or `brew install redis` or any of that. The container's startup script boots Redis as a managed sidecar. If `redis-cli ping` doesn't return `PONG`, flag it to the left-hand helper; it's a container bug, not a lesson step.
- **This starter is shared across all SAAS-140 lessons but Lessons 2-5 each have their own folder** named `saas-140-redis-l2`, `-l3`, `-l4`, `-l5`. Each one is the end state of the previous lesson so you can start a lab mid-course without rebuilding everything.
- **`package.json` lists `ioredis`** — a popular Node Redis client. Lesson 1 uses it from a small script before you wire it into the Hono app. Later lessons use it directly in the API.
- **If you break the starter**, click End Lab and re-launch. The container is thrown away and rebuilt from this folder every launch.
