export interface MonteCarloInputs {
  startingBalance: number;
  annualWithdrawal: number;
  years: number;
  expectedReturn: number;
  returnStdDev: number;
  inflationRate: number;
  trials?: number;
}

export interface MonteCarloPercentiles {
  p10: number[];
  p25: number[];
  p50: number[];
  p75: number[];
  p90: number[];
}

export interface MonteCarloResult {
  successRate: number;
  percentiles: MonteCarloPercentiles;
  trials: number;
}

export function sampleNormal(mean: number, stdDev: number): number {
  let u = 0;
  let v = 0;
  while (u === 0) u = Math.random();
  while (v === 0) v = Math.random();
  const z = Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  return mean + stdDev * z;
}

export function percentile(values: number[], p: number): number {
  if (values.length === 0) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  const idx = (p / 100) * (sorted.length - 1);
  const lo = Math.floor(idx);
  const hi = Math.ceil(idx);
  if (lo === hi) return sorted[lo];
  return sorted[lo] + (idx - lo) * (sorted[hi] - sorted[lo]);
}

export function runMonteCarlo(input: MonteCarloInputs): MonteCarloResult {
  const trials = input.trials ?? 1000;
  const years = input.years;
  const balanceMatrix: number[][] = [];
  let successes = 0;

  for (let t = 0; t < trials; t++) {
    const balances: number[] = [input.startingBalance];
    let balance = input.startingBalance;
    let failed = false;

    for (let y = 1; y <= years; y++) {
      const withdrawalThisYear =
        input.annualWithdrawal * Math.pow(1 + input.inflationRate, y - 1);
      balance -= withdrawalThisYear;

      if (balance <= 0) {
        failed = true;
        for (let f = y; f <= years; f++) balances.push(0);
        break;
      }

      const r = sampleNormal(input.expectedReturn, input.returnStdDev);
      balance = balance * (1 + r);
      balances.push(balance);
    }

    if (!failed && balance > 0) successes++;
    balanceMatrix.push(balances);
  }

  const yearsArr = Array.from({ length: years + 1 }, (_, i) => i);
  const at = (p: number) =>
    yearsArr.map((y) => percentile(balanceMatrix.map((b) => b[y]), p));

  const percentiles: MonteCarloPercentiles = {
    p10: at(10),
    p25: at(25),
    p50: at(50),
    p75: at(75),
    p90: at(90),
  };

  return {
    successRate: successes / trials,
    percentiles,
    trials,
  };
}
