import { describe, it, expect } from 'vitest';
import { planWithdrawal } from './withdrawals';

describe('planWithdrawal', () => {
  it('exhausts cash before touching tax-advantaged accounts', () => {
    const plan = planWithdrawal(
      [
        { id: 1, type: 'cash', balance: 5000 },
        { id: 2, type: 'roth_ira', balance: 100_000 },
      ],
      3000,
      { age: 65, otherOrdinaryIncome: 0 }
    );
    expect(plan.steps).toHaveLength(1);
    expect(plan.steps[0].accountType).toBe('cash');
    expect(plan.steps[0].amount).toBe(3000);
  });

  it('places Roth last in withdrawal order', () => {
    const plan = planWithdrawal(
      [
        { id: 1, type: 'roth_ira', balance: 100_000 },
        { id: 2, type: 'traditional_ira', balance: 100_000 },
      ],
      20_000,
      { age: 65, otherOrdinaryIncome: 30_000 }
    );
    expect(plan.steps[0].accountType).toBe('traditional_ira');
  });

  it('includes RMD step at age 75 even when smaller withdrawals would suffice', () => {
    const plan = planWithdrawal(
      [{ id: 1, type: 'traditional_ira', balance: 500_000 }],
      30_000,
      { age: 75, otherOrdinaryIncome: 30_000 }
    );
    expect(plan.steps[0].rationale).toContain('Required Minimum Distribution');
  });
});
