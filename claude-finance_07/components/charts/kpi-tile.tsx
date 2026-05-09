'use client';

import { Card, Text, Metric, BadgeDelta } from '@tremor/react';

export function KPITile({
  label,
  value,
  delta,
}: {
  label: string;
  value: string;
  delta?: { text: string; type: 'increase' | 'decrease' | 'unchanged' };
}) {
  return (
    <Card className="bg-rs-surface border-rs-border">
      <Text className="text-rs-fg-dim">{label}</Text>
      <Metric className="font-mono tabular text-rs-fg mt-2">{value}</Metric>
      {delta && (
        <BadgeDelta deltaType={delta.type} className="mt-2 font-mono tabular">
          {delta.text}
        </BadgeDelta>
      )}
    </Card>
  );
}