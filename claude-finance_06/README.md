# RetireScope — Lesson 11 Starter

Monte Carlo retirement projection now live: simulation engine in pure TypeScript, Visx fan chart, and a scenario form for entering parameters.

## Getting Started

```bash
npm install
npm run db:generate    # adds scenarios + simulation_results tables
npm run db:migrate
npm run dev
```

In another terminal:

```bash
web-tunnel
```

Open the public URL, navigate to **Projection**, fill in the scenario form, and watch the fan chart render.


> **Don't use the `/proxy/3000/` URL** that VS Code surfaces — Next.js's Turbopack dev server emits absolute `/_next/static/...` URLs that don't resolve through code-server's path-prefixed proxy. Always view the app through the `web-tunnel` ngrok URL instead.


## What's New (Module 5 → Module 6)

- `lib/finance/monte-carlo.ts` — `runMonteCarlo`, `sampleNormal` (Box-Muller), `percentile`
- `lib/finance/monte-carlo.test.ts` — vitest unit tests
- `lib/db/schema.ts` — extended with `scenarios` + `simulation_results` tables and relations
- `lib/actions/projections.ts` — `saveScenarioAndProject` Server Action
- `components/charts/monte-carlo-fan.tsx` — Visx fan chart
- `components/projection/scenario-form.tsx` — form with retirement defaults
- `app/(dashboard)/projection/page.tsx` — full implementation
- `vitest.config.ts` — test runner setup
- New deps: `@visx/*` family; dev: `vitest`

Run tests:

```bash
npm test
```

## What You'll Build in Lesson 11

The tax engine: federal income tax brackets, LTCG brackets, IRS Uniform Lifetime Table for RMDs, the tax-aware withdrawal sequencer, and the Tax Planner page.
