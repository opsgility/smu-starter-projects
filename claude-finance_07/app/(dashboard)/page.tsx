export const dynamic = 'force-dynamic';

import { eq } from 'drizzle-orm';
import { db } from '@/lib/db/client';
import {
  accounts as accountsTable,
  holdings as holdingsTable,
} from '@/lib/db/schema';
import { getQuotes } from '@/lib/quotes/finnhub';
import { computeKPIs } from '@/lib/finance/kpis';
import {
  allocationByAccountType,
  allocationByAssetClass,
} from '@/lib/finance/allocation';
import { KPITile } from '@/components/charts/kpi-tile';
import { AllocationDonut } from '@/components/charts/allocation-donut';
import { EmptyDashboard } from '@/components/holdings/empty-dashboard';
import { LiveHoldingsTable } from '@/components/holdings/live-holdings-table';
import { formatCurrency, formatPercent } from '@/lib/utils/format';

export default async function Dashboard() {
  const rows = await db
    .select()
    .from(holdingsTable)
    .leftJoin(accountsTable, eq(holdingsTable.accountId, accountsTable.id));

  if (rows.length === 0) {
    return <EmptyDashboard />;
  }

  const symbols = rows.map((r) => r.holdings.symbol);
  const quotes = await getQuotes(symbols);

  const enriched = rows.map((r, i) => {
    const q = quotes[i];
    const errored = q && 'error' in q;
    return {
      id: r.holdings.id,
      symbol: r.holdings.symbol,
      account: r.accounts ? r.accounts.name : null,
      accountType: r.accounts?.type ?? 'unknown',
      quantity: r.holdings.quantity,
      costBasis: r.holdings.costBasis,
      assetClass: r.holdings.assetClass,
      price: !errored && q ? q.price : 0,
      changePct: !errored && q ? q.changePct : null,
    };
  });

  const kpis = computeKPIs(enriched);

  const allocationInputs = enriched.map((e) => ({
    quantity: e.quantity,
    assetClass: e.assetClass,
    price: e.price,
    account: { type: e.accountType },
  }));
  const byClass = allocationByAssetClass(allocationInputs);
  const byAccount = allocationByAccountType(allocationInputs);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <KPITile
          label="Total Value"
          value={formatCurrency(kpis.totalValue, true)}
        />
        <KPITile
          label="Today"
          value={formatCurrency(kpis.todayChange.dollars, true)}
          delta={{
            text: formatPercent(kpis.todayChange.percent),
            type:
              kpis.todayChange.dollars > 0
                ? 'increase'
                : kpis.todayChange.dollars < 0
                ? 'decrease'
                : 'unchanged',
          }}
        />
        <KPITile
          label="YTD (vs cost)"
          value={formatCurrency(kpis.ytdChange.dollars, true)}
          delta={{
            text: formatPercent(kpis.ytdChange.percent),
            type:
              kpis.ytdChange.dollars > 0
                ? 'increase'
                : kpis.ytdChange.dollars < 0
                ? 'decrease'
                : 'unchanged',
          }}
        />
        <KPITile
          label="Cash"
          value={formatCurrency(kpis.cashAvailable, true)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <AllocationDonut title="By Asset Class" slices={byClass} />
        <AllocationDonut title="By Account Type" slices={byAccount} />
      </div>

      <LiveHoldingsTable initialHoldings={enriched} />
    </div>
  );
}