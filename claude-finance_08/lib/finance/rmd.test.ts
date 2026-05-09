import { describe, it, expect } from 'vitest';
import { computeRMD } from './rmd';

describe('computeRMD', () => {
  it('returns 0 before age 73', () => {
    expect(computeRMD(1_000_000, 65)).toBe(0);
  });
  it('age 73 with $1.2M → ~$45,283', () => {
    expect(Math.round(computeRMD(1_200_000, 73))).toBe(45_283);
  });
  it('age 80 with $500k → ~$24,752', () => {
    expect(Math.round(computeRMD(500_000, 80))).toBe(24_752);
  });
});
