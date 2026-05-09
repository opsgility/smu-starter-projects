import { Card, Title, DonutChart, Legend } from '@tremor/react';
import { formatCurrency } from '@/lib/utils/format';
import type { AllocationSlice } from '@/lib/finance/allocation';

const COLORS = [
  'indigo',
  'violet',
  'emerald',
  'teal',
  'amber',
  'slate',
  'rose',
  'gray',
];

export function AllocationDonut({
  title,
  slices,
}: {
  title: string;
  slices: AllocationSlice[];
}) {
  return (
    <Card className="bg-rs-surface border-rs-border">
      <Title className="text-rs-fg">{title}</Title>
      <DonutChart
        data={slices}
        category="value"
        index="label"
        valueFormatter={(v: number) => formatCurrency(v)}
        colors={COLORS.slice(0, slices.length)}
        className="mt-4 h-60"
      />
      <Legend
        categories={slices.map((s) => s.label)}
        colors={COLORS.slice(0, slices.length)}
        className="mt-3"
      />
    </Card>
  );
}
