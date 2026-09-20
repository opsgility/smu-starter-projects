import { cn } from '@/lib/utils';
import { formatCurrency, formatPercent } from '@/lib/utils/format';

export function FinancialNumber({
  value,
  type = 'currency',
  signed = false,
  precise = false,
  className,
}: {
  value: number;
  type?: 'currency' | 'percent';
  signed?: boolean;
  precise?: boolean;
  className?: string;
}) {
  const formatted =
    type === 'currency' ? formatCurrency(value, precise) : formatPercent(value);
  const display =
    signed && type === 'currency' && value > 0 ? `+${formatted}` : formatted;
  const colorClass = !signed
    ? 'text-rs-fg'
    : value > 0
    ? 'text-rs-accent'
    : value < 0
    ? 'text-rs-danger'
    : 'text-rs-fg-muted';

  return (
    <span className={cn('font-mono tabular', colorClass, className)}>
      {display}
    </span>
  );
}
