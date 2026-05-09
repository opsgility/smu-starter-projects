# RetireScope — Lesson 13 Starter

Tax-aware withdrawal sequencing: federal income tax brackets, LTCG brackets, IRS Uniform Lifetime Table for RMDs, the tax-aware withdrawal sequencer, and a Tax Planner page.

## Getting Started

```bash
npm install
npm run dev
```

In another terminal:

```bash
web-tunnel
```

Open the public URL, navigate to **Tax Planner**, fill in the form, and run the sequencer.

## What's New (Module 6 → Module 7)

- `lib/finance/tax-brackets.ts` — `computeFederalTax`, `marginalRate`, `computeLTCGTax`
- `lib/finance/rmd.ts` — IRS Uniform Lifetime Table + `computeRMD`
- `lib/finance/withdrawals.ts` — `planWithdrawal` sequencer (cash → RMD → taxable → traditional → Roth)
- `lib/actions/tax-planner.ts` — Server Action that pulls account balances and runs the planner
- `app/(dashboard)/tax-planner/page.tsx` — full implementation
- Unit tests for tax-brackets, rmd, and withdrawals

Run tests:

```bash
npm test
```

## What You'll Build in Lesson 13

The AI Portfolio Assistant: Anthropic Claude with tool use to answer portfolio questions by calling your existing functions.
