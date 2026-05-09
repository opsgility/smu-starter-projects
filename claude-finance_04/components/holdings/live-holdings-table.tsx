'use client';

import { useQuery } from '@tanstack/react-query';

interface HoldingRow {
  id: number;
  symbol: string;
  account?: string | null;
  quantity: string;
  costBasis: string;
  assetClass: string;
  price: number;
  changePct: number | null;
}

interface QuoteResponse {
  quotes: Array<{
    symbol: string;
    price?: number;
    changePct?: number | null;
    error?: string;
  }>;
}

const usd = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 2,
});
const pct = new Intl.NumberFormat('en-US', {
  style: 'percent',
  signDisplay: 'always',
  maximumFractionDigits: 2,
});

export function LiveHoldingsTable({
  initialHoldings,
}: {
  initialHoldings: HoldingRow[];
}) {
  const symbols = initialHoldings.map((h) => h.symbol).join(',');

  const { data } = useQuery<QuoteResponse>({
    queryKey: ['quotes', symbols],
    queryFn: () =>
      fetch(`${process.env.NEXT_PUBLIC_BASE_PATH ?? ''}/api/quotes?symbols=${encodeURIComponent(symbols)}`).then((r) =>
        r.json()
      ),
    initialData: {
      quotes: initialHoldings.map((h) => ({
        symbol: h.symbol,
        price: h.price,
        changePct: h.changePct,
      })),
    },
    refetchInterval: 30_000,
    enabled: symbols.length > 0,
  });

  const quoteBySymbol = new Map(
    (data?.quotes ?? []).map((q) => [q.symbol, q])
  );

  return (
    <div className="bg-rs-surface border border-rs-border rounded-2xl overflow-hidden">
      <table className="w-full text-sm">
        <thead className="text-left text-rs-fg-dim uppercase text-xs tracking-wide bg-rs-bg/40">
          <tr>
            <th className="px-4 py-3">Symbol</th>
            <th className="px-4 py-3">Account</th>
            <th className="px-4 py-3 text-right">Quantity</th>
            <th className="px-4 py-3 text-right">Price</th>
            <th className="px-4 py-3 text-right">Change</th>
            <th className="px-4 py-3 text-right">Value</th>
          </tr>
        </thead>
        <tbody>
          {initialHoldings.map((h) => {
            const q = quoteBySymbol.get(h.symbol);
            const price = q?.price ?? 0;
            const changePct = q?.changePct ?? null;
            const value = price * parseFloat(h.quantity);
            const positive = (changePct ?? 0) >= 0;
            return (
              <tr
                key={h.id}
                className="border-t border-rs-border hover:bg-rs-card transition-colors"
              >
                <td className="px-4 py-3 font-mono font-bold text-rs-fg">
                  {h.symbol}
                </td>
                <td className="px-4 py-3 text-rs-fg-muted">
                  {h.account ?? '—'}
                </td>
                <td className="px-4 py-3 text-right font-mono tabular text-rs-fg">
                  {parseFloat(h.quantity).toFixed(2)}
                </td>
                <td className="px-4 py-3 text-right font-mono tabular text-rs-fg">
                  {q?.error ? (
                    <span className="text-rs-fg-dim text-xs">
                      {q.error}
                    </span>
                  ) : (
                    usd.format(price)
                  )}
                </td>
                <td
                  className={`px-4 py-3 text-right font-mono tabular ${
                    changePct == null
                      ? 'text-rs-fg-dim'
                      : positive
                      ? 'text-rs-accent'
                      : 'text-rs-danger'
                  }`}
                >
                  {changePct != null ? pct.format(changePct) : '—'}
                </td>
                <td className="px-4 py-3 text-right font-mono tabular text-rs-fg">
                  {usd.format(value)}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
