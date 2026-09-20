'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';
import { db } from '@/lib/db/client';
import { holdings } from '@/lib/db/schema';

const CreateHoldingSchema = z.object({
  accountId: z.number().int().positive(),
  symbol: z
    .string()
    .min(1)
    .max(10)
    .transform((s) => s.trim().toUpperCase()),
  name: z.string().optional().nullable(),
  assetClass: z.enum([
    'us_equity',
    'intl_equity',
    'us_bond',
    'intl_bond',
    'reit',
    'cash_equivalent',
    'commodity',
    'other',
  ]),
  quantity: z.number().positive(),
  costBasis: z.number().nonnegative(),
  acquiredAt: z.string().transform((s) => new Date(s)),
});

export type CreateHoldingInput = z.input<typeof CreateHoldingSchema>;

export async function createHolding(input: CreateHoldingInput) {
  const parsed = CreateHoldingSchema.parse(input);

  // Drizzle stores numeric as string to preserve precision; convert at the boundary.
  const [created] = await db
    .insert(holdings)
    .values({
      accountId: parsed.accountId,
      symbol: parsed.symbol,
      name: parsed.name ?? null,
      assetClass: parsed.assetClass,
      quantity: parsed.quantity.toString(),
      costBasis: parsed.costBasis.toString(),
      acquiredAt: parsed.acquiredAt,
    })
    .returning();

  revalidatePath('/accounts');
  revalidatePath(`/accounts/${parsed.accountId}`);
  return created;
}
