'use client';

import { formatCurrency } from '@/lib/utils/format';
import type { MonteCarloResult } from '@/lib/finance/monte-carlo';

interface YearByYearTableProps {
  result: MonteCarloResult;
  startAge: number;
  annualWithdrawal: number;
  inflationRate: number;
}

export function YearByYearTable({
  result,
  startAge,
  annualWithdrawal,
  inflationRate,
}: YearByYearTableProps) {
  // p50.length is years + 1 (index 0 is the starting balance). Iterate from
  // year 1 through the last simulated year so each row represents an
  // end-of-year snapshot.
  const lastYear = result.percentiles.p50.length - 1;
  const rows = Array.from({ length: lastYear }, (_, i) => {
    const year = i + 1;
    const age = startAge + year - 1;
    const withdrawal =
      annualWithdrawal * Math.pow(1 + inflationRate, year - 1);
    return {
      year,
      age,
      withdrawal,
      p10: result.percentiles.p10[year],
      p50: result.percentiles.p50[year],
      p90: result.percentiles.p90[year],
    };
  });

  return (
    <div className="bg-rs-surface border border-rs-border rounded-2xl overflow-hidden">
      <div className="px-4 py-3 border-b border-rs-border">
        <h2 className="text-lg font-semibold text-rs-fg">
          Year-by-Year Breakdown
        </h2>
      </div>
      <div className="max-h-96 overflow-y-auto">
        <table className="w-full text-sm">
          <thead className="text-left text-rs-fg-dim uppercase text-xs tracking-wide bg-rs-card sticky top-0 z-10">
            <tr>
              <th className="px-4 py-3">Year</th>
              <th className="px-4 py-3">Age</th>
              <th className="px-4 py-3 text-right">Withdrawal</th>
              <th className="px-4 py-3 text-right">P10 Balance</th>
              <th className="px-4 py-3 text-right">P50 Balance</th>
              <th className="px-4 py-3 text-right">P90 Balance</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => (
              <tr
                key={r.year}
                className="border-t border-rs-border hover:bg-rs-card transition-colors"
              >
                <td className="px-4 py-3 font-mono tabular text-rs-fg">
                  {r.year}
                </td>
                <td className="px-4 py-3 font-mono tabular text-rs-fg-muted">
                  {r.age}
                </td>
                <td className="px-4 py-3 text-right font-mono tabular text-rs-fg">
                  {formatCurrency(r.withdrawal)}
                </td>
                <td className="px-4 py-3 text-right font-mono tabular text-rs-fg-muted">
                  {formatCurrency(r.p10)}
                </td>
                <td className="px-4 py-3 text-right font-mono tabular text-rs-fg">
                  {formatCurrency(r.p50)}
                </td>
                <td className="px-4 py-3 text-right font-mono tabular text-rs-fg-muted">
                  {formatCurrency(r.p90)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="px-4 py-3 text-xs text-rs-fg-dim border-t border-rs-border">
        Each row shows the end-of-year balance at the 10th, 50th (median), and
        90th percentile across the {result.trials.toLocaleString()} simulated
        futures.
      </p>
    </div>
  );
}
