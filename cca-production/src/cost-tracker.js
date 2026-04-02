// TODO: Step 1 — Implement the CostTracker class
//
// MODEL_PRICING: map of model name -> { inputPerMillion, outputPerMillion }
//   claude-sonnet-4-20250514: $3.00/$15.00
//   claude-haiku-35-20241022: $0.80/$4.00
//   claude-opus-4-20250514: $15.00/$75.00
//
// BATCH_DISCOUNT: 0.5 (50% off for batch API calls)
//
// CostTracker(budgetLimit):
//   record(agentName, model, usage, isBatch): compute cost, push entry, checkBudget()
//   checkBudget(): alert at 75% and 90% of budgetLimit
//   getTotalCost(): sum of all record totalCost values
//   getReport(): return breakdown { totalCalls, totalCost, budgetLimit, byAgent, byModel, alerts }

const MODEL_PRICING = {
  "claude-sonnet-4-20250514": { inputPerMillion: 3.00, outputPerMillion: 15.00 },
  "claude-haiku-35-20241022": { inputPerMillion: 0.80, outputPerMillion: 4.00 },
  "claude-opus-4-20250514": { inputPerMillion: 15.00, outputPerMillion: 75.00 }
};

const BATCH_DISCOUNT = 0.5;

class CostTracker {
  constructor(budgetLimit = null) {
    this.records = [];
    this.budgetLimit = budgetLimit;
    this.alerts = [];
    // TODO: initialize additional state as needed
  }

  record(agentName, model, usage, isBatch = false) {
    // TODO: implement — compute inputCost, outputCost, apply batch discount, push entry
  }

  checkBudget() {
    // TODO: implement — alert at 75% and 90% of budgetLimit (once each)
  }

  getTotalCost() {
    // TODO: implement
    return 0;
  }

  getReport() {
    // TODO: implement — return breakdown by agent and model
    return {
      totalCalls: this.records.length,
      totalCost: this.getTotalCost(),
      budgetLimit: this.budgetLimit,
      byAgent: {},
      byModel: {},
      alerts: this.alerts
    };
  }
}

module.exports = { CostTracker, MODEL_PRICING };
