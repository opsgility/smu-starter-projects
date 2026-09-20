import { describe, it, expect } from 'vitest';
import {
  computeFederalTax,
  marginalRate,
  computeLTCGTax,
} from './tax-brackets';

describe('computeFederalTax', () => {
  it('zero income → zero tax', () => {
    expect(computeFederalTax(0)).toBe(0);
  });
  it('80000 income → ~12653 tax', () => {
    expect(Math.round(computeFederalTax(80_000))).toBe(12_653);
  });
});

describe('marginalRate', () => {
  it('80k → 22%', () => expect(marginalRate(80_000)).toBe(0.22));
  it('250k → 32%', () => expect(marginalRate(250_000)).toBe(0.32));
});

describe('computeLTCGTax', () => {
  it('all LTCG falls in 0% bracket → 0 tax', () => {
    expect(computeLTCGTax(25_000, 20_000)).toBe(0);
  });
  it('all 15% when ordinary income exceeds 0% threshold', () => {
    expect(computeLTCGTax(100_000, 30_000)).toBe(4_500);
  });
});
