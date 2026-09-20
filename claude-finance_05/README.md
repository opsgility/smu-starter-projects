# RetireScope — Lesson 9 Starter

Polished portfolio dashboard with Tremor: KPI tiles, two allocation donut charts (by asset class AND by account type), holdings table, and full empty/loading/error states.

## Getting Started

```bash
npm install
npm run db:migrate    # if needed
npm run dev
```

In another terminal:

```bash
web-tunnel
```

Open the public URL. The dashboard at `/` should render four KPI tiles, two donuts, and the live holdings table — or the empty-state welcome card if no holdings exist yet.


> **Don't use the `/proxy/3000/` URL** that VS Code surfaces — Next.js's Turbopack dev server emits absolute `/_next/static/...` URLs that don't resolve through code-server's path-prefixed proxy. Always view the app through the `web-tunnel` ngrok URL instead.


## What's New (Module 4 → Module 5)

- `lib/utils/format.ts` — `formatCurrency`, `formatPercent`, `formatCurrencyAbbrev`, `formatNumber` (all `Intl.NumberFormat` driven)
- `lib/finance/kpis.ts` — `computeKPIs` for totalValue, todayChange, ytdChange, cashAvailable
- `lib/finance/allocation.ts` — `allocationByAssetClass`, `allocationByAccountType`
- `components/ui/financial-number.tsx` — typed signed-currency / signed-percent component
- `components/charts/kpi-tile.tsx` — Tremor Card + Metric + BadgeDelta wrapper
- `components/charts/allocation-donut.tsx` — Tremor DonutChart with named colors
- `components/holdings/empty-dashboard.tsx` — first-time welcome card
- `app/(dashboard)/page.tsx` — full dashboard rendering KPIs, donuts, holdings table
- `app/(dashboard)/loading.tsx` — skeleton matching the dashboard layout
- `app/(dashboard)/error.tsx` — error boundary with Try again
- New deps: `@tremor/react`, `recharts`

## What You'll Build in Lesson 9

The Monte Carlo retirement projection: simulation engine in pure TypeScript + a Visx fan chart visualizing percentile bands across a 30-year retirement horizon.
