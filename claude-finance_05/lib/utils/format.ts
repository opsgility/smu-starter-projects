const usd = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 0,
});

const usdPrecise = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  maximumFractionDigits: 2,
});

const pctFormatter = new Intl.NumberFormat('en-US', {
  style: 'percent',
  signDisplay: 'always',
  maximumFractionDigits: 2,
});

const numberFormatter = new Intl.NumberFormat('en-US');

export function formatCurrency(n: number, precise = false): string {
  return (precise ? usdPrecise : usd).format(n);
}

export function formatPercent(n: number): string {
  return pctFormatter.format(n);
}

export function formatNumber(n: number): string {
  return numberFormatter.format(n);
}

export function formatCurrencyAbbrev(n: number): string {
  const abs = Math.abs(n);
  const sign = n < 0 ? '-' : '';
  if (abs >= 1_000_000_000) return `${sign}$${(abs / 1_000_000_000).toFixed(2)}B`;
  if (abs >= 1_000_000) return `${sign}$${(abs / 1_000_000).toFixed(2)}M`;
  if (abs >= 1_000) return `${sign}$${(abs / 1_000).toFixed(1)}K`;
  return formatCurrency(n);
}
