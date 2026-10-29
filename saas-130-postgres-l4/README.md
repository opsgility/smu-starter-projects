# SAAS-130 Lesson 4 — Transactions and concurrency

Starter for the fourth lesson of **SAAS-130 — PostgreSQL for SaaS Developers**. This folder is the end-state of Lesson 3 — the Lumen Trail schema lives in a chain of five numbered, reversible migrations under `migrations/`, and a seed script hydrates the tables.

## Scenario

Lumen Trail has a schema that can be rebuilt from zero on any machine with one command. But the application code still runs business operations as isolated SQL statements. "Buy the last Rain Jacket" is actually TWO statements: decrement inventory, create the order. If two users click "buy" at the same instant, both can succeed. In Lesson 4 you fix that with transactions and concurrency control.

## Files

```
saas-130-postgres-l4/
  README.md
  .env.example
  .gitignore
  package.json              # adds node-pg-migrate
  tsconfig.json
  .pgmigraterc.json         # node-pg-migrate config: raw SQL migrations
  migrations/
    0001_create_users.sql
    0002_create_trail_items.sql
    0003_create_orders.sql
    0004_add_category_to_trail_items.sql
    0005_add_notes_to_orders.sql
  src/
    db.ts
    connect.ts
    seed.ts                 # idempotent: 3 users, 5 items, 3 orders
    join.ts
```

## How to run

```
cp .env.example .env
npm run migrate:up          # applies every migration in order
npx tsx src/seed.ts         # loads sample data (idempotent)
npm run join
```

To go back one migration: `npm run migrate:down`. To rebuild from zero: run every migration's down, then every up again. Or just drop the database.

## Notes

- `node-pg-migrate` tracks which migrations have been applied in a `pgmigrations` table it creates automatically.
- Migration file names are `NNNN_name.sql` — the numeric prefix is what defines run order.
- Each file has an `-- Up Migration` block and a `-- Down Migration` block.
