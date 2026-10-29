# SAAS-130 Lesson 3 — Migrations

Starter for the third lesson of **SAAS-130 — PostgreSQL for SaaS Developers**. This folder is the end-state of Lesson 2 — the full three-table schema is in a single hand-run SQL file, and a JOIN script reads data across all three tables.

## Scenario

The Lumen Trail schema is good (every constraint is in the database, FKs link the right rows). But it lives in a single hand-run SQL file. If a teammate pulls this project onto their laptop, there's no way for them to tell whether their database is "the same as yours" — maybe you added a column last week and forgot to tell them. In Lesson 3 you fix this with **migrations**: a chain of numbered, reversible changes that every environment runs through in order.

## Files

```
saas-130-postgres-l3/
  README.md
  .env.example
  .gitignore
  package.json
  tsconfig.json
  sql/
    001_schema.sql          # the full Lesson 2 end-state — three tables + constraints + seed data
  src/
    db.ts
    connect.ts
    setup.ts                # applies sql/001_schema.sql
    join.ts                 # JOIN across orders, users (twice), trail_items
```

## How to run

```
cp .env.example .env
npm run setup
npm run join
```

Expected output: three orders listed with buyer, item, and seller names.

## Notes

- The constraints are now doing real work: `inventory >= 0`, `quantity > 0`, `total_cents >= 0`, and foreign keys that refuse orphan rows.
- `psql $DATABASE_URL` + `\d orders` shows you the table structure with every constraint named.
