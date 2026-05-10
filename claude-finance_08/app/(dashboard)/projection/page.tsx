export const dynamic = 'force-dynamic';

import { eq, desc } from 'drizzle-orm';
import { db } from '@/lib/db/client';
import { scenarios, holdings, accounts, quoteCache } from '@/lib/db/schema';
import {
  runMonteCarlo,
  type MonteCarloResult,
} from '@/lib/finance/monte-carlo';
import { MonteCarloFan } from '@/components/charts/monte-carlo-fan';
import { ScenarioForm } from '@/components/projection/scenario-form';
import type { ScenarioInput } from '@/lib/actions/projections';

function successRateColor(rate: number): string {
  if (rate >= 0.85) return 'text-rs-accent';
  if (rate >= 0.7) return 'text-rs-warning';
  return 'text-rs-danger';
}

async function loadCurrentPortfolioValue(userId: number): Promise<number> {
  const rows = await db
    .select({
      quantity: holdings.quantity,
      costBasis: holdings.costBasis,
      price: quoteCache.price,
    })
    .from(holdings)
    .innerJoin(accounts, eq(accounts.id, holdings.accountId))
    .leftJoin(quoteCache, eq(quoteCache.symbol, holdings.symbol))
    .where(eq(accounts.userId, userId));

  return rows.reduce((sum, h) => {
    const qty = parseFloat(h.quantity);
    if (qty <= 0) return sum;
    const price = h.price
      ? parseFloat(h.price)
      : parseFloat(h.costBasis) / qty;
    return sum + qty * price;
  }, 0);
}

export default async function ProjectionPage() {
  const [scenario] = await db
    .select()
    .from(scenarios)
    .where(eq(scenarios.userId, 1))
    .orderBy(desc(scenarios.createdAt))
    .limit(1);

  const portfolioValue = await loadCurrentPortfolioValue(1);

  let result: MonteCarloResult | null = null;
  let startAge = 65;
  let formDefaults: Partial<ScenarioInput>;

  if (scenario) {
    startAge = scenario.startAge;
    result = runMonteCarlo({
      startingBalance: parseFloat(scenario.startingBalance),
      annualWithdrawal: parseFloat(scenario.annualWithdrawal),
      years: scenario.endAge - scenario.startAge,
      expectedReturn: parseFloat(scenario.expectedReturn),
      returnStdDev: parseFloat(scenario.returnStdDev),
      inflationRate: parseFloat(scenario.inflationRate),
    });
    // Pre-fill the form with the LAST submitted scenario so editing one field
    // and re-running doesn't reset every other field.
    formDefaults = {
      startAge: scenario.startAge,
      endAge: scenario.endAge,
      startingBalance: parseFloat(scenario.startingBalance),
      annualWithdrawal: parseFloat(scenario.annualWithdrawal),
      expectedReturn: parseFloat(scenario.expectedReturn),
      returnStdDev: parseFloat(scenario.returnStdDev),
      inflationRate: parseFloat(scenario.inflationRate),
      withdrawalRule: scenario.withdrawalRule as 'fixed_pct',
    };
  } else {
    // First-run defaults: seed from the imported portfolio + 4% rule.
    formDefaults = {
      startingBalance: portfolioValue,
      annualWithdrawal: portfolioValue * 0.04,
    };
  }

  return (
    <div className="space-y-6">
      <header className="flex items-baseline justify-between">
        <h1 className="text-2xl font-bold text-rs-fg">Retirement Projection</h1>
        {result && (
          <div className="text-right">
            <div className="text-rs-fg-dim text-sm">Success rate</div>
            <div
              className={`font-mono tabular text-2xl ${successRateColor(
                result.successRate
              )}`}
            >
              {(result.successRate * 100).toFixed(0)}%
            </div>
          </div>
        )}
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
          {result ? (
            <MonteCarloFan result={result} startAge={startAge} />
          ) : (
            <div className="bg-rs-surface border border-rs-border rounded-2xl p-12 text-center text-rs-fg-muted">
              Run your first projection to see the fan chart here.
            </div>
          )}
        </div>
        <div>
          <ScenarioForm defaults={formDefaults} />
        </div>
      </div>
    </div>
  );
}
