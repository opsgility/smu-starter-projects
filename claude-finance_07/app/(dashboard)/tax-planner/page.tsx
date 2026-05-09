'use client';

import { useState, useTransition } from 'react';
import { runTaxAwareWithdrawal } from '@/lib/actions/tax-planner';
import type { WithdrawalPlan } from '@/lib/finance/withdrawals';
import { formatCurrency } from '@/lib/utils/format';

const ACCOUNT_TYPE_LABELS: Record<string, string> = {
  taxable: 'Taxable',
  traditional_ira: 'Traditional IRA',
  roth_ira: 'Roth IRA',
  traditional_401k: 'Traditional 401(k)',
  roth_401k: 'Roth 401(k)',
  hsa: 'HSA',
  cash: 'Cash',
};

const DEFAULTS = {
  needed: 40_000,
  age: 65,
  otherOrdinaryIncome: 30_000,
};

export default function TaxPlannerPage() {
  const [plan, setPlan] = useState<WithdrawalPlan | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [, startTransition] = useTransition();
  const [pending, setPending] = useState(false);

  function onSubmit(formData: FormData) {
    setPending(true);
    setError(null);
    startTransition(async () => {
      try {
        const result = await runTaxAwareWithdrawal({
          needed: parseFloat(formData.get('needed') as string),
          age: parseInt(formData.get('age') as string, 10),
          otherOrdinaryIncome: parseFloat(
            formData.get('otherOrdinaryIncome') as string
          ),
        });
        setPlan(result);
      } catch (e) {
        setError((e as Error).message);
      } finally {
        setPending(false);
      }
    });
  }

  return (
    <div className="space-y-6">
      <header className="flex items-baseline justify-between">
        <h1 className="text-2xl font-bold text-rs-fg">Tax Planner</h1>
        {plan && (
          <div className="text-right">
            <div className="text-rs-fg-dim text-sm">Estimated federal tax</div>
            <div className="font-mono tabular text-2xl text-rs-fg">
              {formatCurrency(plan.totalEstimatedFederalTax, true)}
            </div>
          </div>
        )}
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <form
            action={onSubmit}
            className="bg-rs-surface border border-rs-border rounded-2xl p-6 space-y-4"
          >
            <h2 className="text-lg font-bold text-rs-fg">Withdrawal Inputs</h2>

            <div>
              <label className="block text-rs-fg-muted text-sm mb-1.5">
                Cash needed ($)
              </label>
              <input
                name="needed"
                type="number"
                step="1000"
                defaultValue={DEFAULTS.needed}
                className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg font-mono tabular"
              />
            </div>

            <div>
              <label className="block text-rs-fg-muted text-sm mb-1.5">
                Current age
              </label>
              <input
                name="age"
                type="number"
                defaultValue={DEFAULTS.age}
                className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg font-mono tabular"
              />
              <p className="text-rs-fg-dim text-xs mt-1">
                RMDs apply at age 73+
              </p>
            </div>

            <div>
              <label className="block text-rs-fg-muted text-sm mb-1.5">
                Other ordinary income ($)
              </label>
              <input
                name="otherOrdinaryIncome"
                type="number"
                step="1000"
                defaultValue={DEFAULTS.otherOrdinaryIncome}
                className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg font-mono tabular"
              />
              <p className="text-rs-fg-dim text-xs mt-1">
                Social Security, pension, wages — used to stack LTCG and bracket
                ordinary withdrawals.
              </p>
            </div>

            <button
              type="submit"
              disabled={pending}
              className="w-full bg-rs-primary text-rs-primary-fg rounded-lg px-4 py-2 font-medium disabled:opacity-50"
            >
              {pending ? 'Planning…' : 'Run Sequencer'}
            </button>
          </form>
        </div>

        <div className="md:col-span-2">
          {error && (
            <div className="bg-rs-surface border border-rs-danger rounded-2xl p-6 text-rs-danger">
              {error}
            </div>
          )}

          {!plan && !error && (
            <div className="bg-rs-surface border border-rs-border rounded-2xl p-12 text-center text-rs-fg-muted">
              Enter your withdrawal needs and run the sequencer to see the
              recommended pull order: cash → RMD → taxable LTCG → traditional →
              Roth.
            </div>
          )}

          {plan && (
            <div className="bg-rs-surface border border-rs-border rounded-2xl p-6 space-y-4">
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <div className="text-rs-fg-dim text-sm">Needed</div>
                  <div className="font-mono tabular text-rs-fg">
                    {formatCurrency(plan.totalNeeded, true)}
                  </div>
                </div>
                <div>
                  <div className="text-rs-fg-dim text-sm">Withdrawn</div>
                  <div className="font-mono tabular text-rs-fg">
                    {formatCurrency(plan.totalWithdrawn, true)}
                  </div>
                </div>
                <div>
                  <div className="text-rs-fg-dim text-sm">Shortfall</div>
                  <div
                    className={`font-mono tabular ${
                      plan.shortfall > 0 ? 'text-rs-danger' : 'text-rs-fg'
                    }`}
                  >
                    {formatCurrency(plan.shortfall, true)}
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-rs-fg font-semibold mb-2">
                  Recommended sequence
                </h3>
                {plan.steps.length === 0 ? (
                  <p className="text-rs-fg-muted text-sm">
                    No withdrawals needed.
                  </p>
                ) : (
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-rs-fg-dim text-left border-b border-rs-border">
                        <th className="pb-2 pr-3">Account</th>
                        <th className="pb-2 pr-3 text-right">Amount</th>
                        <th className="pb-2 pr-3 text-right">Est. tax</th>
                        <th className="pb-2">Rationale</th>
                      </tr>
                    </thead>
                    <tbody>
                      {plan.steps.map((step, i) => (
                        <tr key={i} className="border-b border-rs-border/50">
                          <td className="py-2 pr-3 text-rs-fg">
                            {ACCOUNT_TYPE_LABELS[step.accountType] ??
                              step.accountType}
                            <span className="text-rs-fg-dim text-xs ml-1">
                              #{step.accountId}
                            </span>
                          </td>
                          <td className="py-2 pr-3 text-right font-mono tabular text-rs-fg">
                            {formatCurrency(step.amount, true)}
                          </td>
                          <td className="py-2 pr-3 text-right font-mono tabular text-rs-fg">
                            {formatCurrency(step.estimatedFederalTax, true)}
                          </td>
                          <td className="py-2 text-rs-fg-muted">
                            {step.rationale}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
