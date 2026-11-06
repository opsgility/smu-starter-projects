# agy-100-l4 — Meridian Devworks internal API skeleton

Starter project for **AGY-100 Lesson 8 — "Run two agents in parallel on different endpoints"** in the Google Antigravity IDE path.

You're playing **Marcus** at Meridian Devworks. The team's internal API has two un-implemented endpoints — pagination on `/users`, filtering on `/products`. Both changes are independent (different endpoints, different files when the agents emit their diffs, different query parameters). Your task in the lab is to run TWO agent conversations in parallel, one per endpoint, each in its own worktree, and watch the Agent Manager coordinate your review attention between them.

## Shape

- `app.js` — Express skeleton with two un-implemented endpoints (`GET /users`, `GET /products`), both currently returning the full data. TODO comments explain the target behavior.
- `data/users.json` — 20 Meridian team members.
- `data/products.json` — 15 warehouse SKUs with four categories (pallet, wrapping, label, box, equipment).
- `package.json` — Express 4.18.0.
- `README.md` — this file.

## Current behavior

```
npm install
npm start
```

Then:
```
curl http://127.0.0.1:3000/users
```
Returns all 20 users as one array. No pagination.

```
curl http://127.0.0.1:3000/products
```
Returns all 15 products as one array. No category filter.

## Target behavior after the lab

- `GET /users?page=2&limit=5` returns `{ page: 2, limit: 5, total: 20, items: [5 users] }` (users 6-10 by id).
- `GET /products?category=pallet` returns `{ filter: { category: "pallet" }, items: [3 products] }` (SKU-001, SKU-002, SKU-010).
- Both endpoints handle missing / malformed query params gracefully.

## Why TWO conversations in parallel?

The lab exercises the Agent Manager + parallel-worktrees pattern from Lesson 7. Pagination and filtering are **independent** — different endpoints, different TODO blocks in `app.js`, different query shapes. That means they parallelize cleanly: two worktrees, two conversations, both ship in the wall-clock time of the slowest single one.

If the student runs them SERIALLY instead, both still work — but the student does not get the Lesson 7 teaching reinforcement. The lab's reflection exercise asks the student to notice the overlap moment where both conversations were in `Executing` simultaneously.

## Deployment path

This starter is auto-downloaded onto the lab VM at `C:\labs\agy-100-l4\` via the SkillMeUp `downloadfiles.ps1` CSE pipeline.

Related: `Plans/ANTIGRAVITY_IDE_PATH_PLAN.md` in the `opsgilitylabs-core-claude` repo.
