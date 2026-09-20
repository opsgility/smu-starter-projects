// Drizzle's `numeric()` columns are returned as strings to preserve precision.
// Most finance code wants real numbers, so we centralize the conversion here
// instead of sprinkling `parseFloat(row.quantity)` calls across every file.

export interface NumericHolding {
  quantity: number;
  costBasis: number;
}

export function asNumericHolding<
  T extends { quantity: string; costBasis: string }
>(h: T): Omit<T, 'quantity' | 'costBasis'> & NumericHolding {
  return { ...h, quantity: parseFloat(h.quantity), costBasis: parseFloat(h.costBasis) };
}
