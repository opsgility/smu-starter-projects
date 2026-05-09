import { computeFederalTax, computeLTCGTax } from './tax-brackets';
import { computeRMD, RMD_START_AGE } from './rmd';

export type WithdrawalAccountType =
  | 'taxable'
  | 'traditional_ira'
  | 'roth_ira'
  | 'traditional_401k'
  | 'roth_401k'
  | 'hsa'
  | 'cash';

export interface AccountWithBalance {
  id: number;
  type: WithdrawalAccountType;
  balance: number;
  costBasis?: number;
}

export interface WithdrawalStep {
  accountId: number;
  accountType: WithdrawalAccountType;
  amount: number;
  estimatedFederalTax: number;
  rationale: string;
}

export interface WithdrawalPlan {
  totalNeeded: number;
  totalWithdrawn: number;
  steps: WithdrawalStep[];
  totalEstimatedFederalTax: number;
  shortfall: number;
}

export function planWithdrawal(
  accounts: AccountWithBalance[],
  needed: number,
  ctx: { age: number; otherOrdinaryIncome: number }
): WithdrawalPlan {
  let remaining = needed;
  const steps: WithdrawalStep[] = [];
  let totalTax = 0;
  let runningOrdinary = ctx.otherOrdinaryIncome;

  // 1. Cash first — no tax friction
  for (const acc of accounts
    .filter((a) => a.type === 'cash')
    .sort((a, b) => b.balance - a.balance)) {
    if (remaining <= 0) break;
    const w = Math.min(acc.balance, remaining);
    if (w <= 0) continue;
    steps.push({
      accountId: acc.id,
      accountType: acc.type,
      amount: w,
      estimatedFederalTax: 0,
      rationale: 'Cash — no tax cost',
    });
    remaining -= w;
  }

  // 2. RMD-required accounts (must take regardless of preference)
  if (ctx.age >= RMD_START_AGE) {
    for (const acc of accounts.filter(
      (a) => a.type === 'traditional_ira' || a.type === 'traditional_401k'
    )) {
      const rmd = computeRMD(acc.balance, ctx.age);
      if (rmd <= 0) continue;
      const tax =
        computeFederalTax(runningOrdinary + rmd) -
        computeFederalTax(runningOrdinary);
      steps.push({
        accountId: acc.id,
        accountType: acc.type,
        amount: rmd,
        estimatedFederalTax: tax,
        rationale: `Required Minimum Distribution at age ${ctx.age}`,
      });
      remaining -= rmd;
      totalTax += tax;
      runningOrdinary += rmd;
    }
  }

  // 3. Taxable brokerage with LTCG
  for (const acc of accounts.filter((a) => a.type === 'taxable')) {
    if (remaining <= 0) break;
    const w = Math.min(acc.balance, remaining);
    if (w <= 0) continue;
    const gainRatio = acc.costBasis
      ? Math.max(0, (acc.balance - acc.costBasis) / acc.balance)
      : 0;
    const ltcg = w * gainRatio;
    const tax = computeLTCGTax(runningOrdinary, ltcg);
    steps.push({
      accountId: acc.id,
      accountType: acc.type,
      amount: w,
      estimatedFederalTax: tax,
      rationale: 'Taxable brokerage (LTCG-bracket aware)',
    });
    remaining -= w;
    totalTax += tax;
  }

  // 4. Traditional IRA / 401(k) — ordinary income
  for (const acc of accounts.filter(
    (a) => a.type === 'traditional_ira' || a.type === 'traditional_401k'
  )) {
    if (remaining <= 0) break;
    const w = Math.min(acc.balance, remaining);
    if (w <= 0) continue;
    const tax =
      computeFederalTax(runningOrdinary + w) -
      computeFederalTax(runningOrdinary);
    steps.push({
      accountId: acc.id,
      accountType: acc.type,
      amount: w,
      estimatedFederalTax: tax,
      rationale: 'Traditional retirement account (ordinary income tax)',
    });
    remaining -= w;
    totalTax += tax;
    runningOrdinary += w;
  }

  // 5. Roth — last (tax-free; preserve growth)
  for (const acc of accounts.filter(
    (a) => a.type === 'roth_ira' || a.type === 'roth_401k'
  )) {
    if (remaining <= 0) break;
    const w = Math.min(acc.balance, remaining);
    if (w <= 0) continue;
    steps.push({
      accountId: acc.id,
      accountType: acc.type,
      amount: w,
      estimatedFederalTax: 0,
      rationale: 'Roth account (tax-free withdrawal)',
    });
    remaining -= w;
  }

  const totalWithdrawn = steps.reduce((s, x) => s + x.amount, 0);
  return {
    totalNeeded: needed,
    totalWithdrawn,
    steps,
    totalEstimatedFederalTax: totalTax,
    shortfall: Math.max(0, needed - totalWithdrawn),
  };
}
