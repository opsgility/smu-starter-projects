import { eq, sql } from 'drizzle-orm';
import { db } from '@/lib/db/client';
import { accounts, holdings, quoteCache } from '@/lib/db/schema';
import { computeKPIs } from '@/lib/finance/kpis';
import { allocationByAssetClass } from '@/lib/finance/allocation';
import { runMonteCarlo } from '@/lib/finance/monte-carlo';
import { runTaxAwareWithdrawal } from '@/lib/actions/tax-planner';

const USER_ID = 1;

async function loadHoldingsWithQuotes() {
  const rows = await db
    .select({
      accountId: holdings.accountId,
      accountType: accounts.type,
      symbol: holdings.symbol,
      assetClass: holdings.assetClass,
      quantity: holdings.quantity,
      costBasis: holdings.costBasis,
      price: quoteCache.price,
      changePct: quoteCache.changePct,
    })
    .from(holdings)
    .innerJoin(accounts, eq(accounts.id, holdings.accountId))
    .leftJoin(quoteCache, eq(quoteCache.symbol, holdings.symbol))
    .where(eq(accounts.userId, USER_ID));

  return rows.map((r) => ({
    accountId: r.accountId,
    accountType: r.accountType,
    symbol: r.symbol,
    assetClass: r.assetClass,
    quantity: r.quantity,
    costBasis: r.costBasis,
    price: r.price ? parseFloat(r.price) : parseFloat(r.costBasis) / parseFloat(r.quantity),
    changePct: r.changePct ? parseFloat(r.changePct) : null,
  }));
}

export async function handleToolCall(
  name: string,
  input: Record<string, unknown>
): Promise<string> {
  try {
    switch (name) {
      case 'get_portfolio_summary': {
        const enriched = await loadHoldingsWithQuotes();
        const kpis = computeKPIs(enriched);
        return JSON.stringify(kpis);
      }
      case 'list_accounts': {
        const rows = await db
          .select({
            id: accounts.id,
            name: accounts.name,
            type: accounts.type,
            institution: accounts.institution,
            balance: sql<string>`COALESCE(SUM(CAST(${holdings.quantity} AS NUMERIC) * COALESCE(CAST(${quoteCache.price} AS NUMERIC), CAST(${holdings.costBasis} AS NUMERIC) / NULLIF(CAST(${holdings.quantity} AS NUMERIC), 0))), 0)`,
          })
          .from(accounts)
          .leftJoin(holdings, eq(holdings.accountId, accounts.id))
          .leftJoin(quoteCache, eq(quoteCache.symbol, holdings.symbol))
          .where(eq(accounts.userId, USER_ID))
          .groupBy(accounts.id);
        return JSON.stringify(
          rows.map((r) => ({ ...r, balance: parseFloat(r.balance) }))
        );
      }
      case 'get_allocation': {
        const enriched = await loadHoldingsWithQuotes();
        return JSON.stringify(allocationByAssetClass(enriched));
      }
      case 'run_projection': {
        const result = runMonteCarlo({
          startingBalance: input.startingBalance as number,
          annualWithdrawal: input.annualWithdrawal as number,
          years: input.years as number,
          expectedReturn: input.expectedReturn as number,
          returnStdDev: input.returnStdDev as number,
          inflationRate: 0.025,
        });
        return JSON.stringify({
          successRate: result.successRate,
          finalP10: result.percentiles.p10[result.percentiles.p10.length - 1],
          finalP50: result.percentiles.p50[result.percentiles.p50.length - 1],
          finalP90: result.percentiles.p90[result.percentiles.p90.length - 1],
        });
      }
      case 'plan_withdrawal': {
        const plan = await runTaxAwareWithdrawal({
          needed: input.needed as number,
          age: input.age as number,
          otherOrdinaryIncome: input.otherOrdinaryIncome as number,
        });
        return JSON.stringify(plan);
      }
      default:
        return JSON.stringify({ error: `Unknown tool: ${name}` });
    }
  } catch (e) {
    return JSON.stringify({ error: (e as Error).message });
  }
}
