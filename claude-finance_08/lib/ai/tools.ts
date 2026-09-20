import type Anthropic from '@anthropic-ai/sdk';

export const TOOLS: Anthropic.Tool[] = [
  {
    name: 'get_portfolio_summary',
    description:
      'Returns portfolio KPIs across all accounts. Fields: totalValue (current market value), todayChange ({dollars, percent} day-on-day move from quote_cache change_pct), gainsSincePurchase ({dollars, percent} unrealized gain — totalValue minus total cost basis; this is NOT a year-to-date figure, it is cumulative since each holding was purchased), cashAvailable (sum of cash_equivalent holdings). When reporting gainsSincePurchase to the user, call it "gain since purchase" or "unrealized gain" — never call it "YTD" because cost basis is not anchored to start-of-year.',
    input_schema: {
      type: 'object' as const,
      properties: {},
      required: [],
    },
  },
  {
    name: 'list_accounts',
    description:
      'Lists all of the user\'s accounts with type, institution, and current balance.',
    input_schema: {
      type: 'object' as const,
      properties: {},
      required: [],
    },
  },
  {
    name: 'get_allocation',
    description:
      'Returns asset allocation breakdown by asset class (equity, bond, cash, etc.) with both dollar amounts and percentages.',
    input_schema: {
      type: 'object' as const,
      properties: {},
      required: [],
    },
  },
  {
    name: 'run_projection',
    description:
      'Runs a Monte Carlo retirement projection. Returns success rate (probability of not running out of money) and the year-by-year percentile bands.',
    input_schema: {
      type: 'object' as const,
      properties: {
        startingBalance: {
          type: 'number',
          description: 'Starting portfolio balance in dollars.',
        },
        annualWithdrawal: {
          type: 'number',
          description: 'Inflation-adjusted annual withdrawal in today\'s dollars.',
        },
        years: {
          type: 'number',
          description: 'Number of years to project (e.g. 30 for retirement at 65 living to 95).',
        },
        expectedReturn: {
          type: 'number',
          description: 'Expected annual real return as a decimal (0.05 = 5%).',
        },
        returnStdDev: {
          type: 'number',
          description: 'Annual return standard deviation as a decimal (0.15 = 15%).',
        },
      },
      required: ['startingBalance', 'annualWithdrawal', 'years', 'expectedReturn', 'returnStdDev'],
    },
  },
  {
    name: 'plan_withdrawal',
    description:
      'Runs the tax-aware withdrawal sequencer for the requested amount. Returns the per-account withdrawal plan and total estimated federal tax.',
    input_schema: {
      type: 'object' as const,
      properties: {
        needed: {
          type: 'number',
          description: 'Total dollars needed for the year.',
        },
        age: {
          type: 'number',
          description: 'User\'s current age (RMDs apply at 73+).',
        },
        otherOrdinaryIncome: {
          type: 'number',
          description: 'Other ordinary income (Social Security, pension, etc.) for tax-bracket stacking.',
        },
      },
      required: ['needed', 'age', 'otherOrdinaryIncome'],
    },
  },
];
