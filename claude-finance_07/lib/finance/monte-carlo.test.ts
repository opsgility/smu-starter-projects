import { describe, it, expect } from 'vitest';
import { runMonteCarlo, sampleNormal, percentile } from './monte-carlo';

describe('percentile', () => {
  it('returns the middle for p50 of [1..9]', () => {
    expect(percentile([1, 2, 3, 4, 5, 6, 7, 8, 9], 50)).toBe(5);
  });
  it('interpolates between values', () => {
    expect(percentile([0, 100], 50)).toBe(50);
    expect(percentile([0, 100], 25)).toBe(25);
  });
});

describe('sampleNormal', () => {
  it('over 10000 samples, mean approximates the target', () => {
    const samples = Array.from({ length: 10000 }, () => sampleNormal(0.07, 0.15));
    const mean = samples.reduce((s, x) => s + x, 0) / samples.length;
    expect(Math.abs(mean - 0.07)).toBeLessThan(0.01);
  });
});

describe('runMonteCarlo', () => {
  it('returns the expected shape', () => {
    const result = runMonteCarlo({
      startingBalance: 1_000_000,
      annualWithdrawal: 40_000,
      years: 30,
      expectedReturn: 0.07,
      returnStdDev: 0.15,
      inflationRate: 0.03,
      trials: 100,
    });
    expect(result.trials).toBe(100);
    expect(result.successRate).toBeGreaterThanOrEqual(0);
    expect(result.successRate).toBeLessThanOrEqual(1);
    expect(result.percentiles.p50).toHaveLength(31);
    expect(result.percentiles.p10[0]).toBe(1_000_000);
    expect(result.percentiles.p90[0]).toBe(1_000_000);
  });

  it('higher withdrawal reduces success rate', () => {
    const easy = runMonteCarlo({
      startingBalance: 1_000_000,
      annualWithdrawal: 30_000,
      years: 30,
      expectedReturn: 0.07,
      returnStdDev: 0.15,
      inflationRate: 0.03,
      trials: 200,
    });
    const hard = runMonteCarlo({
      startingBalance: 1_000_000,
      annualWithdrawal: 60_000,
      years: 30,
      expectedReturn: 0.07,
      returnStdDev: 0.15,
      inflationRate: 0.03,
      trials: 200,
    });
    expect(easy.successRate).toBeGreaterThan(hard.successRate);
  });
});
