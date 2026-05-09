// IRS Uniform Lifetime Table excerpt (post SECURE 2.0 — RMDs start at age 73)

export const RMD_START_AGE = 73;

const UNIFORM_LIFETIME_TABLE: Record<number, number> = {
  73: 26.5,
  74: 25.5,
  75: 24.6,
  76: 23.7,
  77: 22.9,
  78: 22.0,
  79: 21.1,
  80: 20.2,
  81: 19.4,
  82: 18.5,
  83: 17.7,
  84: 16.8,
  85: 16.0,
  86: 15.2,
  87: 14.4,
  88: 13.7,
  89: 12.9,
  90: 12.2,
  91: 11.5,
  92: 10.8,
  93: 10.1,
  94: 9.5,
  95: 8.9,
  96: 8.4,
  97: 7.8,
  98: 7.3,
  99: 6.8,
  100: 6.4,
};

export function computeRMD(
  priorYearEndBalance: number,
  age: number
): number {
  if (age < RMD_START_AGE) return 0;
  const period =
    UNIFORM_LIFETIME_TABLE[age] ?? UNIFORM_LIFETIME_TABLE[100];
  return priorYearEndBalance / period;
}

export function isRmdYear(age: number): boolean {
  return age >= RMD_START_AGE;
}
