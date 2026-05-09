'use server';

import { z } from 'zod';
import { eq } from 'drizzle-orm';
import { revalidatePath } from 'next/cache';
import { db } from '@/lib/db/client';
import { accounts } from '@/lib/db/schema';

const CreateAccountSchema = z.object({
  userId: z.number().int().positive(),
  name: z.string().min(1, 'Name is required').max(200),
  type: z.enum([
    'taxable',
    'traditional_ira',
    'roth_ira',
    'traditional_401k',
    'roth_401k',
    'hsa',
    'cash',
  ]),
  institution: z.string().max(100).optional().nullable(),
});

export type CreateAccountInput = z.infer<typeof CreateAccountSchema>;

export async function createAccount(input: CreateAccountInput) {
  const data = CreateAccountSchema.parse(input);
  const [created] = await db.insert(accounts).values(data).returning();
  revalidatePath('/accounts');
  return created;
}

export async function deleteAccount(id: number) {
  await db.delete(accounts).where(eq(accounts.id, id));
  revalidatePath('/accounts');
}
