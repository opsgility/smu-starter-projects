import { redirect } from 'next/navigation';
import { db } from '@/lib/db/client';
import { accounts as accountsTable } from '@/lib/db/schema';
import { createHolding } from '@/lib/actions/holdings';

const ASSET_CLASS_OPTIONS = [
  { value: 'us_equity', label: 'US Equity' },
  { value: 'intl_equity', label: 'International Equity' },
  { value: 'us_bond', label: 'US Bond' },
  { value: 'intl_bond', label: 'International Bond' },
  { value: 'reit', label: 'REIT' },
  { value: 'cash_equivalent', label: 'Cash Equivalent' },
  { value: 'commodity', label: 'Commodity' },
  { value: 'other', label: 'Other' },
] as const;

export default async function NewHoldingPage({
  searchParams,
}: {
  searchParams: Promise<{ accountId?: string }>;
}) {
  const { accountId: defaultAccountIdParam } = await searchParams;
  const accounts = await db.select().from(accountsTable);

  async function handleSubmit(formData: FormData) {
    'use server';
    const accountId = parseInt(formData.get('accountId') as string, 10);
    await createHolding({
      accountId,
      symbol: formData.get('symbol') as string,
      name: (formData.get('name') as string) || null,
      assetClass: formData.get('assetClass') as 'us_equity',
      quantity: parseFloat(formData.get('quantity') as string),
      costBasis: parseFloat(formData.get('costBasis') as string),
      acquiredAt: formData.get('acquiredAt') as string,
    });
    redirect(`/accounts/${accountId}`);
  }

  return (
    <div className="max-w-md mx-auto mt-8">
      <h1 className="text-2xl font-bold text-rs-fg mb-6">Add Holding</h1>
      {accounts.length === 0 ? (
        <p className="text-rs-fg-muted">
          You need to create an account first before adding holdings.
        </p>
      ) : (
        <form
          action={handleSubmit}
          className="bg-rs-surface border border-rs-border rounded-2xl p-6 space-y-4"
        >
          <div>
            <label className="block text-rs-fg-muted text-sm mb-1.5">
              Account
            </label>
            <select
              name="accountId"
              required
              defaultValue={defaultAccountIdParam}
              className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg"
            >
              {accounts.map((a) => (
                <option key={a.id} value={a.id}>
                  {a.name} ({a.type})
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-rs-fg-muted text-sm mb-1.5">
              Symbol
            </label>
            <input
              name="symbol"
              required
              placeholder="VTI"
              style={{ textTransform: 'uppercase' }}
              className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg font-mono"
            />
          </div>
          <div>
            <label className="block text-rs-fg-muted text-sm mb-1.5">
              Name (optional)
            </label>
            <input
              name="name"
              placeholder="Vanguard Total Stock Market ETF"
              className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg"
            />
          </div>
          <div>
            <label className="block text-rs-fg-muted text-sm mb-1.5">
              Asset Class
            </label>
            <select
              name="assetClass"
              required
              className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg"
            >
              {ASSET_CLASS_OPTIONS.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-rs-fg-muted text-sm mb-1.5">
                Quantity
              </label>
              <input
                name="quantity"
                required
                type="number"
                step="0.000001"
                min="0"
                className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg font-mono tabular"
              />
            </div>
            <div>
              <label className="block text-rs-fg-muted text-sm mb-1.5">
                Cost Basis
              </label>
              <input
                name="costBasis"
                required
                type="number"
                step="0.01"
                min="0"
                className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg font-mono tabular"
              />
            </div>
          </div>
          <div>
            <label className="block text-rs-fg-muted text-sm mb-1.5">
              Acquired On
            </label>
            <input
              name="acquiredAt"
              required
              type="date"
              className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-rs-primary text-rs-primary-fg rounded-lg px-4 py-2 font-medium"
          >
            Create Holding
          </button>
        </form>
      )}
    </div>
  );
}
