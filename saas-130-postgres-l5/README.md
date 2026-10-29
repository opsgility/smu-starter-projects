# SAAS-130 Lesson 5 — Query performance

Starter for the fifth lesson of **SAAS-130 — PostgreSQL for SaaS Developers**. This folder is the end-state of Lesson 4 — the checkout flow is transactional, uses `SELECT ... FOR UPDATE` + a `version` column, and refuses to let two users buy the same scarce item.

## Scenario

Lumen Trail's checkout works. It's correct under concurrency. But Lumen Trail now has 10,000 items in the catalog and 50,000 orders in history, and the "list this seller's recent orders" page takes four seconds to load. In Lesson 5 you learn the three tools that make slow queries fast: **EXPLAIN** (reading query plans), **indexes** (B-tree lookups vs full table scans), and recognizing the **N+1** anti-pattern.

## Files

```
saas-130-postgres-l5/
  README.md
  .env.example
  .gitignore
  package.json
  tsconfig.json
  .pgmigraterc.json
  migrations/
    0001_create_users.sql
    0002_create_trail_items.sql       # includes version + category columns
    0003_create_orders.sql             # includes notes column
  src/
    db.ts
    connect.ts
    seed.ts                 # 3 users, 5 items, 1 Rain Jacket with inventory=1
    checkout.ts             # transactional buy() with FOR UPDATE + version
    race.ts                 # two concurrent buy()s on the scarce Rain Jacket
```

## How to run

```
cp .env.example .env
npm run migrate:up
npm run seed
npm run checkout        # one buy() demonstrating the flow
npm run race            # two concurrent buys of the last Rain Jacket — exactly 1 wins
```

## Notes

- The race-demo output should show exactly one `ok: true` and one `ok: false` with `reason: "sold_out"`.
- The checkout code is deliberately didactic — real production uses a thinner wrapper, but every production codebase makes the same four decisions: BEGIN, lock, update-with-version, INSERT, COMMIT or ROLLBACK.
