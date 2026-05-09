# RetireScope — Lesson 5 Starter

Now with a real data layer: PostgreSQL (auto-provisioned in the lab as `labdb`), Drizzle ORM with TypeScript-first schema, and Server Actions for accounts and holdings CRUD.

## Getting Started

```bash
npm install
```

Generate and apply the first migration:

```bash
npm run db:generate
npm run db:migrate
```

Seed a test user:

```bash
npm run db:seed
```

Then run the dev server:

```bash
npm run dev
```

In another terminal:

```bash
web-tunnel
```

Open the public URL. Click **Accounts** in the sidebar — you should see an empty state. Click **+ Add Account** and create one.


> **Don't use the `/proxy/3000/` URL** that VS Code surfaces — Next.js's Turbopack dev server emits absolute `/_next/static/...` URLs that don't resolve through code-server's path-prefixed proxy. Always view the app through the `web-tunnel` ngrok URL instead.


## What's New (Module 2 → Module 3)

- `lib/db/schema.ts` — full Drizzle schema (users, accounts, holdings, quote_cache) with pgEnums and relations
- `lib/db/client.ts` — Drizzle client singleton with globalThis pool cache for dev hot reload
- `lib/db/seed.ts` — inserts a single test user
- `drizzle.config.ts` — drizzle-kit configuration
- `lib/actions/accounts.ts` — Server Actions for create/delete with Zod validation
- `lib/actions/holdings.ts` — Server Action for create with Zod validation
- `app/(dashboard)/accounts/page.tsx` — real list view with empty state
- `app/(dashboard)/accounts/new/page.tsx` — form with inline Server Action
- `app/(dashboard)/accounts/[id]/page.tsx` — detail view with holdings table
- `app/(dashboard)/holdings/new/page.tsx` — holding creation form

## What You'll Build in Lesson 5

Live stock quotes via the free Finnhub API, cached in PostgreSQL with a 60-second TTL. Real prices flowing into your holdings table.
