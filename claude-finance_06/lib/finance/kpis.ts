export interface DashboardKPIs {
  totalValue: number;
  todayChange: { dollars: number; percent: number };
  ytdChange: { dollars: number; percent: number };
  cashAvailable: number;
}

export interface KPIHolding {
  quantity: string;
  costBasis: string;
  assetClass: string;
  price: number;
  changePct: number | null;
  ytdPrice?: number;
}

export function computeKPIs(holdings: KPIHolding[]): DashboardKPIs {
  const totalValue = holdings.reduce(
    (s, h) => s + h.price * parseFloat(h.quantity),
    0
  );

  const todayChangeDollars = holdings.reduce((s, h) => {
    if (h.changePct == null || h.price <= 0) return s;
    const yesterdayPrice = h.price / (1 + h.changePct);
    return s + (h.price - yesterdayPrice) * parseFloat(h.quantity);
  }, 0);
  const todayDenom = totalValue - todayChangeDollars;
  const todayChangePct = todayDenom > 0 ? todayChangeDollars / todayDenom : 0;

  // Year-to-date change requires a baseline price snapshot.
  // For v1, we approximate using cost basis. The Performance module (capstone
  // option A) replaces this with TWR computed from a transactions log.
  const ytdValueStart = holdings.reduce(
    (s, h) =>
      s +
      (h.ytdPrice != null
        ? h.ytdPrice * parseFloat(h.quantity)
        : parseFloat(h.costBasis)),
    0
  );
  const ytdChangeDollars = totalValue - ytdValueStart;
  const ytdChangePct = ytdValueStart > 0 ? ytdChangeDollars / ytdValueStart : 0;

  const cashAvailable = holdings
    .filter((h) => h.assetClass === 'cash_equivalent')
    .reduce((s, h) => s + h.price * parseFloat(h.quantity), 0);

  return {
    totalValue,
    todayChange: { dollars: todayChangeDollars, percent: todayChangePct },
    ytdChange: { dollars: ytdChangeDollars, percent: ytdChangePct },
    cashAvailable,
  };
}
