'use server';

import { eq, sql } from 'drizzle-orm';
import { db } from '@/lib/db/client';
import { accounts, holdings, quoteCache } from '@/lib/db/schema';
import {
  planWithdrawal,
  type AccountWithBalance,
  type WithdrawalAccountType,
  type WithdrawalPlan,
} from '@/lib/finance/withdrawals';

export interface TaxPlanInput {
  needed: number;
  age: number;
  otherOrdinaryIncome: number;
}

export async function runTaxAwareWithdrawal(
  input: TaxPlanInput
): Promise<WithdrawalPlan> {
  // Pull each account's summed market value from holdings × quote_cache
  const rows = await db
    .select({
      id: accounts.id,
      type: accounts.type,
      balance: sql<string>`COALESCE(SUM(CAST(${holdings.quantity} AS NUMERIC) * COALESCE(CAST(${quoteCache.price} AS NUMERIC), CAST(${holdings.costBasis} AS NUMERIC) / NULLIF(CAST(${holdings.quantity} AS NUMERIC), 0))), 0)`,
      costBasis: sql<string>`COALESCE(SUM(CAST(${holdings.costBasis} AS NUMERIC)), 0)`,
    })
    .from(accounts)
    .leftJoin(holdings, eq(holdings.accountId, accounts.id))
    .leftJoin(quoteCache, eq(quoteCache.symbol, holdings.symbol))
    .where(eq(accounts.userId, 1))
    .groupBy(accounts.id);

  const inputs: AccountWithBalance[] = rows.map((r) => ({
    id: r.id,
    type: r.type as WithdrawalAccountType,
    balance: parseFloat(r.balance),
    costBasis: parseFloat(r.costBasis),
  }));

  return planWithdrawal(inputs, input.needed, {
    age: input.age,
    otherOrdinaryIncome: input.otherOrdinaryIncome,
  });
}
