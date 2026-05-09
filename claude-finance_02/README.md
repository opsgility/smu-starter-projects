# RetireScope — Lesson 3 Starter

Next.js 16 scaffold with the RetireScope design system, dark mode, and sidebar nav. Five core routes are stubbed (Dashboard, Accounts, Projection, Tax Planner, Assistant) — you'll fill them in starting with Lesson 3.

## Getting Started

```bash
npm install
npm run dev
```

In another terminal:

```bash
web-tunnel
```

Open the public URL — you should see the dark dashboard shell with the sidebar.


> **Don't use the `/proxy/3000/` URL** that VS Code surfaces — Next.js's Turbopack dev server emits absolute `/_next/static/...` URLs that don't resolve through code-server's path-prefixed proxy. Always view the app through the `web-tunnel` ngrok URL instead.


## What's New (Module 1 → Module 2)

- `app/globals.css` — full `@theme` block with brand, surface, text, and font tokens
- `app/layout.tsx` — Geist + JetBrains Mono fonts, forced `dark` class on `<html>`
- `app/(dashboard)/` — route group with sidebar layout
  - `layout.tsx` — sidebar + main content area
  - `page.tsx` — Dashboard (test KPI card)
  - `accounts/page.tsx`, `projection/page.tsx`, `tax-planner/page.tsx`, `assistant/page.tsx` — placeholders
- `components/sidebar.tsx` — Client Component with `usePathname` and active-state highlighting

## What You'll Build in Lesson 3

The accounts and holdings data layer: Drizzle schema + Postgres + Server Actions + CRUD UI. By the end, you'll be able to add real accounts and holdings via forms.
