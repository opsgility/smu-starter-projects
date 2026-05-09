// 2026 federal tax brackets — illustrative (verify against current IRS Rev. Proc. before production use)

export interface TaxBracket {
  min: number;
  max: number;
  rate: number;
}

export const FEDERAL_BRACKETS_2026_SINGLE: TaxBracket[] = [
  { min: 0, max: 11_600, rate: 0.10 },
  { min: 11_600, max: 47_150, rate: 0.12 },
  { min: 47_150, max: 100_525, rate: 0.22 },
  { min: 100_525, max: 191_950, rate: 0.24 },
  { min: 191_950, max: 243_725, rate: 0.32 },
  { min: 243_725, max: 609_350, rate: 0.35 },
  { min: 609_350, max: Infinity, rate: 0.37 },
];

export const LTCG_BRACKETS_2026_SINGLE: TaxBracket[] = [
  { min: 0, max: 48_350, rate: 0.0 },
  { min: 48_350, max: 533_400, rate: 0.15 },
  { min: 533_400, max: Infinity, rate: 0.2 },
];

export const STANDARD_DEDUCTION_2026_SINGLE = 14_800;

export function computeFederalTax(
  taxableIncome: number,
  brackets: TaxBracket[] = FEDERAL_BRACKETS_2026_SINGLE
): number {
  if (taxableIncome <= 0) return 0;
  let tax = 0;
  for (const b of brackets) {
    if (taxableIncome <= b.min) break;
    const taxedAtThisBracket = Math.min(taxableIncome, b.max) - b.min;
    tax += taxedAtThisBracket * b.rate;
  }
  return tax;
}

export function marginalRate(
  taxableIncome: number,
  brackets: TaxBracket[] = FEDERAL_BRACKETS_2026_SINGLE
): number {
  for (const b of brackets) {
    if (taxableIncome >= b.min && taxableIncome < b.max) return b.rate;
  }
  return brackets[brackets.length - 1].rate;
}

export function effectiveRate(
  taxableIncome: number,
  brackets: TaxBracket[] = FEDERAL_BRACKETS_2026_SINGLE
): number {
  if (taxableIncome <= 0) return 0;
  return computeFederalTax(taxableIncome, brackets) / taxableIncome;
}

/**
 * Long-term capital gains tax. LTCG is "stacked" on top of ordinary income —
 * each dollar of LTCG is taxed at the LTCG bracket where it lands when added
 * after ordinaryIncome.
 */
export function computeLTCGTax(
  ordinaryIncome: number,
  ltcgAmount: number,
  ltcgBrackets: TaxBracket[] = LTCG_BRACKETS_2026_SINGLE
): number {
  if (ltcgAmount <= 0) return 0;

  let tax = 0;
  let remaining = ltcgAmount;
  let stackTop = ordinaryIncome;

  for (const b of ltcgBrackets) {
    if (stackTop + remaining <= b.min) break;
    if (stackTop >= b.max) continue;

    const headroom = b.max - Math.max(stackTop, b.min);
    const taxed = Math.min(remaining, headroom);
    if (taxed > 0) {
      tax += taxed * b.rate;
      remaining -= taxed;
      stackTop += taxed;
    } else {
      stackTop = b.max;
    }
    if (remaining <= 0) break;
  }

  return tax;
}
