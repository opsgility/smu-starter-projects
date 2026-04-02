const { AgentError, ErrorCategory, EscalationTrigger, classifyError } = require("./error-types");

// TODO: Step 2 — Implement the ErrorChain class
//
// record(agentName, error):
//   - Determine category (use error.category or classifyError())
//   - Push entry: { agent, category, message, timestamp, retryable, context }
//   - Check if agentErrors for this agent+category exceeds EscalationTrigger.maxRetries
//   - If so, push to escalations and return { shouldEscalate: true, escalation }
//   - Otherwise return { shouldEscalate: false, entry }
//
// getReport():
//   - Return { totalErrors, totalEscalations, byCategory, errors, escalations }

class ErrorChain {
  constructor() {
    this.errors = [];
    this.escalations = [];
    // TODO: initialize additional state as needed
  }

  record(agentName, error) {
    // TODO: implement
  }

  getReport() {
    // TODO: implement
    return {
      totalErrors: this.errors.length,
      totalEscalations: this.escalations.length,
      byCategory: {},
      errors: this.errors,
      escalations: this.escalations
    };
  }
}

module.exports = { ErrorChain };
