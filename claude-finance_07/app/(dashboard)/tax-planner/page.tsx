export const dynamic = 'force-dynamic';

import { eq, desc } from 'drizzle-orm';
import { db } from '@/lib/db/client';
import {
  scenarios,
  holdings,
  accounts,
  quoteCache,
} from '@/lib/db/schema';
import { TaxPlannerForm } from '@/components/tax-planner/tax-planner-form';

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

export default async function TaxPlannerPage() {
  // Use the same default-withdrawal logic as /projection so the two pages stay
  // in sync. Priority: last saved scenario's annualWithdrawal → 4% of current
  // portfolio value → fallback constant inside the form.
  const [scenario] = await db
    .select()
    .from(scenarios)
    .where(eq(scenarios.userId, 1))
    .orderBy(desc(scenarios.createdAt))
    .limit(1);

  let defaultNeeded = 0;
  let defaultAge: number | undefined;

  if (scenario) {
    defaultNeeded = parseFloat(scenario.annualWithdrawal);
    defaultAge = scenario.startAge;
  } else {
    const portfolioValue = await loadCurrentPortfolioValue(1);
    defaultNeeded = portfolioValue * 0.04;
  }

  return <TaxPlannerForm defaultNeeded={defaultNeeded} defaultAge={defaultAge} />;
}
