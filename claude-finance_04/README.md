# RetireScope — Lesson 7 Starter

Live stock quotes are now flowing — Finnhub integration with Postgres-backed cache, TanStack Query polling, and a live holdings table.

## Getting Started

```bash
npm install
```

Make sure your `.env.local` has both vars:

```
DATABASE_URL="postgresql://coder:coder@localhost:5432/labdb"
FINNHUB_API_KEY=your_free_finnhub_key
```

If you don't have a Finnhub key, sign up free at `https://finnhub.io/register` — no credit card required.

```bash
npm run db:migrate    # if you haven't already
npm run dev
```

In another terminal:

```bash
web-tunnel
```

Open the public URL, navigate to an account detail page, and watch the live prices populate. The TanStack Query polls `/api/quotes` every 30 seconds.


> **Don't use the `/proxy/3000/` URL** that VS Code surfaces — Next.js's Turbopack dev server emits absolute `/_next/static/...` URLs that don't resolve through code-server's path-prefixed proxy. Always view the app through the `web-tunnel` ngrok URL instead.


## What's New (Module 3 → Module 4)

- `lib/quotes/finnhub.ts` — `fetchQuote`, `getQuote` (with 60s DB cache), `getQuotes`, typed `QuoteError` codes
- `app/api/quotes/route.ts` — GET handler at `/api/quotes?symbols=VTI,BND` returning JSON
- `app/providers.tsx` — TanStack Query `QueryClientProvider` (wrapped on layout)
- `app/layout.tsx` — wraps body in `<Providers>`
- `components/holdings/live-holdings-table.tsx` — Client Component using `useQuery` with 30s polling
- `app/(dashboard)/accounts/[id]/page.tsx` — Server Component that loads holdings + quotes and renders the live table
- New dep: `@tanstack/react-query`

## What You'll Build in Lesson 7

The polished portfolio dashboard: KPI tiles, allocation pies (by asset class AND account type), a holdings table with sparklines, and the empty / loading / error states that take it from "feature complete" to "ship quality."
