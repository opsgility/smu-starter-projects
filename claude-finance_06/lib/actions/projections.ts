'use server';

import { eq } from 'drizzle-orm';
import { revalidatePath } from 'next/cache';
import { db } from '@/lib/db/client';
import { scenarios, simulationResults } from '@/lib/db/schema';
import { runMonteCarlo, type MonteCarloResult } from '@/lib/finance/monte-carlo';

export interface ScenarioInput {
  startAge: number;
  endAge: number;
  startingBalance: number;
  annualWithdrawal: number;
  expectedReturn: number;
  returnStdDev: number;
  inflationRate: number;
  withdrawalRule: 'fixed_pct' | 'guardrails' | 'vpw';
}

export async function saveScenarioAndProject(
  input: ScenarioInput
): Promise<MonteCarloResult> {
  const [scenario] = await db
    .insert(scenarios)
    .values({
      userId: 1,
      name: 'Active scenario',
      startAge: input.startAge,
      endAge: input.endAge,
      startingBalance: input.startingBalance.toString(),
      annualWithdrawal: input.annualWithdrawal.toString(),
      expectedReturn: input.expectedReturn.toString(),
      returnStdDev: input.returnStdDev.toString(),
      inflationRate: input.inflationRate.toString(),
      withdrawalRule: input.withdrawalRule,
    })
    .returning();

  const result = runMonteCarlo({
    startingBalance: input.startingBalance,
    annualWithdrawal: input.annualWithdrawal,
    years: input.endAge - input.startAge,
    expectedReturn: input.expectedReturn,
    returnStdDev: input.returnStdDev,
    inflationRate: input.inflationRate,
  });

  await db.insert(simulationResults).values({
    scenarioId: scenario.id,
    trials: result.trials,
    successRate: result.successRate.toString(),
    percentilesJson: result.percentiles,
  });

  revalidatePath('/projection');
  return result;
}

export async function loadLatestScenario() {
  const [scenario] = await db
    .select()
    .from(scenarios)
    .where(eq(scenarios.userId, 1))
    .orderBy(scenarios.createdAt)
    .limit(1);
  return scenario ?? null;
}
