import type Anthropic from '@anthropic-ai/sdk';

export const TOOLS: Anthropic.Tool[] = [
  {
    name: 'get_portfolio_summary',
    description:
      'Returns the user\'s total portfolio value, today\'s change, YTD change, and cash available across all accounts.',
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
