export const dynamic = 'force-dynamic';

import Link from 'next/link';
import { eq } from 'drizzle-orm';
import { notFound } from 'next/navigation';
import { db } from '@/lib/db/client';
import { accounts as accountsTable, holdings as holdingsTable } from '@/lib/db/schema';

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

      <div className="bg-rs-surface border border-rs-border rounded-2xl overflow-hidden">
        {holdings.length === 0 ? (
          <p className="text-rs-fg-muted text-sm p-6">
            No holdings yet — add one to get started.
          </p>
        ) : (
          <table className="w-full text-sm">
            <thead className="text-left text-rs-fg-dim uppercase text-xs tracking-wide bg-rs-bg/40">
              <tr>
                <th className="px-4 py-3">Symbol</th>
                <th className="px-4 py-3">Asset Class</th>
                <th className="px-4 py-3 text-right">Quantity</th>
                <th className="px-4 py-3 text-right">Cost Basis</th>
              </tr>
            </thead>
            <tbody>
              {holdings.map((h) => (
                <tr key={h.id} className="border-t border-rs-border">
                  <td className="px-4 py-3 font-mono font-bold text-rs-fg">
                    {h.symbol}
                  </td>
                  <td className="px-4 py-3 text-rs-fg-muted">{h.assetClass}</td>
                  <td className="px-4 py-3 text-right font-mono tabular text-rs-fg">
                    {parseFloat(h.quantity).toFixed(2)}
                  </td>
                  <td className="px-4 py-3 text-right font-mono tabular text-rs-fg">
                    ${parseFloat(h.costBasis).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}