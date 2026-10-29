# SAAS-130 Lesson 2 — Schema design

Starter for the second lesson of **SAAS-130 — PostgreSQL for SaaS Developers**. This folder is the end-state of Lesson 1 — a single `trail_items` table lives in Postgres with five seed rows, and two Node scripts prove the plumbing works.

## Scenario

The Lumen Trail catalog is persisted now, but the schema is pretending to be a spreadsheet — one table, no relationships, no constraints beyond `NOT NULL`. In Lesson 2 you redesign it the way a real SaaS backend does: a `users` table, a `trail_items` table that knows which user owns each listing, and an `orders` table that references both.

## Files

```
saas-130-postgres-l2/
  README.md
  .env.example
  .gitignore
  package.json
  tsconfig.json
  sql/
    001_trail_items.sql     # Lesson 1 end-state schema
  src/
    db.ts                   # shared pool
    connect.ts              # smoke test
    setup.ts                # applies sql/001_trail_items.sql
    list-items.ts           # SELECT every item
```

## How to run

```
cp .env.example .env
npm run setup           # applies the Lesson 1 schema + seed rows
npm run list-items      # SELECT every item
```

## Notes

- The `lumentrail` database must already exist (created in Lesson 1 Exercise 1).
- `psql $DATABASE_URL` from the terminal gives you an interactive session for anything the Node scripts don't cover.
