import {
  pgTable,
  pgEnum,
  serial,
  integer,
  text,
  numeric,
  timestamp,
  boolean,
  jsonb,
  index,
} from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';

export const accountTypeEnum = pgEnum('account_type', [
  'taxable',
  'traditional_ira',
  'roth_ira',
  'traditional_401k',
  'roth_401k',
  'hsa',
  'cash',
]);

export const assetClassEnum = pgEnum('asset_class', [
  'us_equity',
  'intl_equity',
  'us_bond',
  'intl_bond',
  'reit',
  'cash_equivalent',
  'commodity',
  'other',
]);

export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  email: text('email').notNull().unique(),
  birthYear: integer('birth_year').notNull(),
  retirementAge: integer('retirement_age').notNull().default(65),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});

export const accounts = pgTable(
  'accounts',
  {
    id: serial('id').primaryKey(),
    userId: integer('user_id').notNull().references(() => users.id),
    name: text('name').notNull(),
    type: accountTypeEnum('type').notNull(),
    institution: text('institution'),
    isActive: boolean('is_active').notNull().default(true),
    createdAt: timestamp('created_at').notNull().defaultNow(),
    updatedAt: timestamp('updated_at').notNull().defaultNow(),
  },
  (t) => ({ userIdx: index('accounts_user_idx').on(t.userId) })
);

export const holdings = pgTable(
  'holdings',
  {
    id: serial('id').primaryKey(),
    accountId: integer('account_id')
      .notNull()
      .references(() => accounts.id, { onDelete: 'cascade' }),
    symbol: text('symbol').notNull(),
    name: text('name'),
    assetClass: assetClassEnum('asset_class').notNull(),
    quantity: numeric('quantity', { precision: 18, scale: 6 }).notNull(),
    costBasis: numeric('cost_basis', { precision: 18, scale: 2 }).notNull(),
    acquiredAt: timestamp('acquired_at').notNull(),
    notes: text('notes'),
  },
  (t) => ({
    accountIdx: index('holdings_account_idx').on(t.accountId),
    symbolIdx: index('holdings_symbol_idx').on(t.symbol),
  })
);

export const quoteCache = pgTable('quote_cache', {
  symbol: text('symbol').primaryKey(),
  price: numeric('price', { precision: 18, scale: 4 }).notNull(),
  changePct: numeric('change_pct', { precision: 8, scale: 4 }),
  fetchedAt: timestamp('fetched_at').notNull().defaultNow(),
});

export const scenarios = pgTable('scenarios', {
  id: serial('id').primaryKey(),
  userId: integer('user_id').notNull().references(() => users.id),
  name: text('name').notNull(),
  startAge: integer('start_age').notNull(),
  endAge: integer('end_age').notNull(),
  startingBalance: numeric('starting_balance', { precision: 18, scale: 2 }).notNull(),
  annualWithdrawal: numeric('annual_withdrawal', { precision: 18, scale: 2 }).notNull(),
  expectedReturn: numeric('expected_return', { precision: 6, scale: 4 }).notNull(),
  returnStdDev: numeric('return_std_dev', { precision: 6, scale: 4 }).notNull(),
  inflationRate: numeric('inflation_rate', { precision: 6, scale: 4 }).notNull(),
  withdrawalRule: text('withdrawal_rule').notNull(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});

export const simulationResults = pgTable('simulation_results', {
  id: serial('id').primaryKey(),
  scenarioId: integer('scenario_id').notNull().references(() => scenarios.id),
  trials: integer('trials').notNull(),
  successRate: numeric('success_rate', { precision: 5, scale: 4 }).notNull(),
  percentilesJson: jsonb('percentiles_json').notNull(),
  createdAt: timestamp('created_at').notNull().defaultNow(),
});

export const usersRelations = relations(users, ({ many }) => ({
  accounts: many(accounts),
  scenarios: many(scenarios),
}));

export const accountsRelations = relations(accounts, ({ one, many }) => ({
  user: one(users, { fields: [accounts.userId], references: [users.id] }),
  holdings: many(holdings),
}));

export const holdingsRelations = relations(holdings, ({ one }) => ({
  account: one(accounts, {
    fields: [holdings.accountId],
    references: [accounts.id],
  }),
}));

export const scenariosRelations = relations(scenarios, ({ one, many }) => ({
  user: one(users, { fields: [scenarios.userId], references: [users.id] }),
  simulationResults: many(simulationResults),
}));

export const simulationResultsRelations = relations(
  simulationResults,
  ({ one }) => ({
    scenario: one(scenarios, {
      fields: [simulationResults.scenarioId],
      references: [scenarios.id],
    }),
  })
);

export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
export type Account = typeof accounts.$inferSelect;
export type NewAccount = typeof accounts.$inferInsert;
export type Holding = typeof holdings.$inferSelect;
export type NewHolding = typeof holdings.$inferInsert;
export type QuoteCacheRow = typeof quoteCache.$inferSelect;
export type Scenario = typeof scenarios.$inferSelect;
export type NewScenario = typeof scenarios.$inferInsert;
export type SimulationResultRow = typeof simulationResults.$inferSelect;
