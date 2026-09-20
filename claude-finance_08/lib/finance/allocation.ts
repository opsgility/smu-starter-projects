export interface AllocationSlice {
  label: string;
  value: number;
  percent: number;
}

const ASSET_CLASS_LABELS: Record<string, string> = {
  us_equity: 'US Equity',
  intl_equity: 'Intl Equity',
  us_bond: 'US Bond',
  intl_bond: 'Intl Bond',
  reit: 'REIT',
  cash_equivalent: 'Cash',
  commodity: 'Commodity',
  other: 'Other',
};

const ACCOUNT_TYPE_LABELS: Record<string, string> = {
  taxable: 'Taxable',
  traditional_ira: 'Traditional IRA',
  roth_ira: 'Roth IRA',
  traditional_401k: 'Traditional 401k',
  roth_401k: 'Roth 401k',
  hsa: 'HSA',
  cash: 'Cash',
};

interface HoldingForAllocation {
  quantity: string;
  assetClass: string;
  price: number;
  account?: { type: string };
}

function bySlug(
  holdings: HoldingForAllocation[],
  groupKey: (h: HoldingForAllocation) => string,
  labels: Record<string, string>
): AllocationSlice[] {
  const totals = new Map<string, number>();
  let grand = 0;
  for (const h of holdings) {
    const v = h.price * parseFloat(h.quantity);
    const key = groupKey(h);
    totals.set(key, (totals.get(key) ?? 0) + v);
    grand += v;
  }
  return [...totals.entries()]
    .map(([slug, value]) => ({
      label: labels[slug] ?? slug,
      value,
      percent: grand > 0 ? value / grand : 0,
    }))
    .sort((a, b) => b.value - a.value);
}

export function allocationByAssetClass(
  holdings: HoldingForAllocation[]
): AllocationSlice[] {
  return bySlug(holdings, (h) => h.assetClass, ASSET_CLASS_LABELS);
}

export function allocationByAccountType(
  holdings: HoldingForAllocation[]
): AllocationSlice[] {
  return bySlug(
    holdings,
    (h) => h.account?.type ?? 'unknown',
    ACCOUNT_TYPE_LABELS
  );
}
