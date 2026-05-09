import {
  pgTable,
  pgEnum,
  serial,
  integer,
  text,
  numeric,
  timestamp,
  boolean,
  index,
} from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';

// -------------------------------------------------------------------------
// Enums
// -------------------------------------------------------------------------

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

// -------------------------------------------------------------------------
// Tables
// -------------------------------------------------------------------------

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
  (t) => ({
    userIdx: index('accounts_user_idx').on(t.userId),
  })
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

// -------------------------------------------------------------------------
// Relations
// -------------------------------------------------------------------------

export const usersRelations = relations(users, ({ many }) => ({
  accounts: many(accounts),
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

// -------------------------------------------------------------------------
// Inferred types — use these everywhere instead of writing them by hand
// -------------------------------------------------------------------------

export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;

export type Account = typeof accounts.$inferSelect;
export type NewAccount = typeof accounts.$inferInsert;

export type Holding = typeof holdings.$inferSelect;
export type NewHolding = typeof holdings.$inferInsert;

export type QuoteCacheRow = typeof quoteCache.$inferSelect;
