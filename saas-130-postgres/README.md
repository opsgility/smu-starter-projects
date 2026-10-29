# SAAS-130 Lesson 1 — Postgres starter

Starter for the first lesson of **SAAS-130 — PostgreSQL for SaaS Developers**. This folder has one job: *verify the plumbing works*. The container has Postgres 16 running on `localhost:5432`; this starter has a tiny Node script that connects to it and prints the server time.

## Scenario

**Lumen Trail** — the camping-gear subscription business from SAAS-120 — is moving its catalog off an in-memory Map and onto a real database. In Lesson 1 you confirm the plumbing (database, user, connection string, Node driver) and run your first SQL. In Lessons 2-5 you build the full schema, add migrations, make the checkout flow transactional, and tune queries for scale.

## Files

```
saas-130-postgres/
  README.md                 # this file
  .env.example              # DATABASE_URL — copy to .env
  .gitignore
  package.json              # pg, dotenv — preinstalled in the container
  tsconfig.json
  src/
    db.ts                   # shared Postgres pool
    connect.ts              # smoke test: connects, prints server time
```

## How to run

The ClaudeSaasStack container boots Postgres automatically. You still need to copy the env file once:

```
cp .env.example .env
```

Then connect:

```
npm run connect
```

Expected output: `connected to Postgres. Server time: 2026-10-29 ...`.

## Authentication

Local only — the container's Postgres uses `postgres`/`postgres` as the superuser. Nothing here reaches the internet.

## Notes

- `node-pg-migrate` arrives in Lesson 3. For Lesson 1 you'll run SQL by hand through `psql`.
- The `lumentrail` database doesn't exist on first boot — Lesson 1 Exercise 1 creates it.
