export const dynamic = 'force-dynamic';

import Link from 'next/link';
import { eq } from 'drizzle-orm';
import { notFound } from 'next/navigation';
import { db } from '@/lib/db/client';
import {
  accounts as accountsTable,
  holdings as holdingsTable,
} from '@/lib/db/schema';
import { getQuotes } from '@/lib/quotes/finnhub';
import { LiveHoldingsTable } from '@/components/holdings/live-holdings-table';

export default async function AccountDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const accountId = parseInt(id, 10);
  if (Number.isNaN(accountId)) notFound();

  const [account] = await db
    .select()
    .from(accountsTable)
    .where(eq(accountsTable.id, accountId))
    .limit(1);

  if (!account) notFound();

  const holdings = await db
    .select()
    .from(holdingsTable)
    .where(eq(holdingsTable.accountId, accountId));

  const symbols = holdings.map((h) => h.symbol);
  const quotes = symbols.length > 0 ? await getQuotes(symbols) : [];

  const enriched = holdings.map((h, i) => {
    const q = quotes[i];
    const errored = q && 'error' in q;
    return {
      id: h.id,
      symbol: h.symbol,
      account: account.name,
      quantity: h.quantity,
      costBasis: h.costBasis,
      assetClass: h.assetClass,
      price: !errored && q ? q.price : 0,
      changePct: !errored && q ? q.changePct : null,
    };
  });

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-rs-fg">{account.name}</h1>
          <p className="text-rs-fg-muted text-sm mt-1">
            {account.type} · {account.institution ?? 'No institution set'}
          </p>
        </div>
        <Link
          href={`/holdings/new?accountId=${account.id}`}
          className="inline-flex items-center gap-2 rounded-lg bg-rs-primary text-rs-primary-fg px-4 py-2 text-sm font-medium"
        >
          + Add Holding
        </Link>
      </div>

      {enriched.length === 0 ? (
        <p className="text-rs-fg-muted text-sm">
          No holdings yet — add one to get started.
        </p>
      ) : (
        <LiveHoldingsTable initialHoldings={enriched} />
      )}
    </div>
  );
}