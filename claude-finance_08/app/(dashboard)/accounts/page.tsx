import Link from 'next/link';
import { Wallet } from 'lucide-react';
import { eq } from 'drizzle-orm';
import { db } from '@/lib/db/client';
import { accounts as accountsTable } from '@/lib/db/schema';

const TYPE_LABELS: Record<string, string> = {
  taxable: 'Taxable',
  traditional_ira: 'Traditional IRA',
  roth_ira: 'Roth IRA',
  traditional_401k: 'Traditional 401k',
  roth_401k: 'Roth 401k',
  hsa: 'HSA',
  cash: 'Cash',
};

export default async function AccountsPage() {
  const accounts = await db
    .select()
    .from(accountsTable)
    .where(eq(accountsTable.isActive, true))
    .orderBy(accountsTable.name);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-rs-fg">Accounts</h1>
        <Link
          href="/accounts/new"
          className="inline-flex items-center gap-2 rounded-lg bg-rs-primary text-rs-primary-fg px-4 py-2 text-sm font-medium"
        >
          + Add Account
        </Link>
      </div>

      {accounts.length === 0 ? (
        <div className="bg-rs-surface border border-rs-border rounded-2xl p-12 text-center max-w-md mx-auto">
          <div className="inline-flex size-16 items-center justify-center rounded-2xl bg-rs-card mb-4">
            <Wallet className="size-8 text-rs-fg-muted" />
          </div>
          <h2 className="text-xl font-bold text-rs-fg mb-2">No accounts yet</h2>
          <p className="text-rs-fg-muted text-sm mb-6 max-w-prose mx-auto">
            Add your first account to start tracking your portfolio.
          </p>
          <Link
            href="/accounts/new"
            className="inline-flex items-center gap-2 rounded-lg bg-rs-primary text-rs-primary-fg px-4 py-2 text-sm font-medium"
          >
            + Add Account
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {accounts.map((account) => (
            <Link
              key={account.id}
              href={`/accounts/${account.id}`}
              className="bg-rs-surface border border-rs-border rounded-2xl p-5 hover:bg-rs-card transition-colors"
            >
              <div className="text-rs-fg font-bold">{account.name}</div>
              <div className="text-rs-fg-dim text-xs uppercase tracking-wide mt-1">
                {TYPE_LABELS[account.type] ?? account.type}
              </div>
              {account.institution && (
                <div className="text-rs-fg-muted text-sm mt-2">
                  {account.institution}
                </div>
              )}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
