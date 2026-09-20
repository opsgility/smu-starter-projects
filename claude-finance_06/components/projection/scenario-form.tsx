'use client';

import { useState, useTransition } from 'react';
import {
  saveScenarioAndProject,
  type ScenarioInput,
} from '@/lib/actions/projections';

interface ScenarioFormProps {
  defaults?: Partial<ScenarioInput>;
}

const FALLBACK_DEFAULTS: ScenarioInput = {
  startAge: 65,
  endAge: 95,
  startingBalance: 1_000_000,
  annualWithdrawal: 40_000,
  expectedReturn: 0.07,
  returnStdDev: 0.15,
  inflationRate: 0.03,
  withdrawalRule: 'fixed_pct',
};

export function ScenarioForm({ defaults = {} }: ScenarioFormProps = {}) {
  const [, startTransition] = useTransition();
  const [pending, setPending] = useState(false);

  const d: ScenarioInput = { ...FALLBACK_DEFAULTS, ...defaults };

  function onSubmit(formData: FormData) {
    setPending(true);
    startTransition(async () => {
      try {
        await saveScenarioAndProject({
          startAge: parseInt(formData.get('startAge') as string, 10),
          endAge: parseInt(formData.get('endAge') as string, 10),
          startingBalance: parseFloat(formData.get('startingBalance') as string),
          annualWithdrawal: parseFloat(
            formData.get('annualWithdrawal') as string
          ),
          expectedReturn:
            parseFloat(formData.get('expectedReturn') as string) / 100,
          returnStdDev: parseFloat(formData.get('returnStdDev') as string) / 100,
          inflationRate:
            parseFloat(formData.get('inflationRate') as string) / 100,
          withdrawalRule: formData.get('withdrawalRule') as 'fixed_pct',
        });
      } finally {
        setPending(false);
      }
    });
  }

  return (
    <form
      action={onSubmit}
      className="bg-rs-surface border border-rs-border rounded-2xl p-6 space-y-4"
    >
      <h2 className="text-lg font-bold text-rs-fg">Scenario Parameters</h2>
      <p className="text-rs-fg-dim text-xs -mt-2">
        Pre-filled from your last run (or your current portfolio on first use). Edit any field and re-run.
      </p>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-rs-fg-muted text-sm mb-1.5">Start age</label>
          <input
            name="startAge"
            type="number"
            defaultValue={d.startAge}
            className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg font-mono tabular"
          />
        </div>
        <div>
          <label className="block text-rs-fg-muted text-sm mb-1.5">End age</label>
          <input
            name="endAge"
            type="number"
            defaultValue={d.endAge}
            className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg font-mono tabular"
          />
        </div>
      </div>

      <div>
        <label className="block text-rs-fg-muted text-sm mb-1.5">
          Starting balance ($)
        </label>
        <input
          name="startingBalance"
          type="number"
          step="1000"
          defaultValue={Math.round(d.startingBalance)}
          className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg font-mono tabular"
        />
      </div>

      <div>
        <label className="block text-rs-fg-muted text-sm mb-1.5">
          Annual withdrawal ($, in starting-year dollars)
        </label>
        <input
          name="annualWithdrawal"
          type="number"
          step="1000"
          defaultValue={Math.round(d.annualWithdrawal)}
          className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg font-mono tabular"
        />
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div>
          <label className="block text-rs-fg-muted text-sm mb-1.5">
            Expected return (%)
          </label>
          <input
            name="expectedReturn"
            type="number"
            step="0.1"
            defaultValue={(d.expectedReturn * 100).toFixed(1)}
            className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg font-mono tabular"
          />
        </div>
        <div>
          <label className="block text-rs-fg-muted text-sm mb-1.5">Std dev (%)</label>
          <input
            name="returnStdDev"
            type="number"
            step="0.5"
            defaultValue={(d.returnStdDev * 100).toFixed(1)}
            className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg font-mono tabular"
          />
        </div>
        <div>
          <label className="block text-rs-fg-muted text-sm mb-1.5">Inflation (%)</label>
          <input
            name="inflationRate"
            type="number"
            step="0.1"
            defaultValue={(d.inflationRate * 100).toFixed(1)}
            className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg font-mono tabular"
          />
        </div>
      </div>

      <div>
        <label className="block text-rs-fg-muted text-sm mb-1.5">
          Withdrawal rule
        </label>
        <select
          name="withdrawalRule"
          defaultValue={d.withdrawalRule}
          className="w-full bg-rs-card border border-rs-border rounded-lg px-3 py-2 text-rs-fg"
        >
          <option value="fixed_pct">Fixed (4% rule)</option>
          <option value="guardrails">Guyton-Klinger guardrails</option>
          <option value="vpw">VPW (Variable Percentage Withdrawal)</option>
        </select>
      </div>

      <button
        type="submit"
        disabled={pending}
        className="w-full bg-rs-primary text-rs-primary-fg rounded-lg px-4 py-2 font-medium disabled:opacity-50"
      >
        {pending ? 'Running 1,000 simulations…' : 'Run Projection'}
      </button>
    </form>
  );
}
