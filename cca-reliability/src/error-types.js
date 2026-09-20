// TODO: Step 1 — Define structured error types for the DocStream pipeline
//
// AgentError(category, message, context): extends Error
//   - Sets name, category, context, timestamp, retryable (true for transient/resource)
//
// ErrorCategory: { TRANSIENT, VALIDATION, RESOURCE, FATAL }
//
// EscalationTrigger: map of category -> { maxRetries, escalateAfter }
//
// classifyError(error): map HTTP status codes to ErrorCategory
//   - 429/529 -> TRANSIENT, 400 -> VALIDATION, 413/quota -> RESOURCE, 500+ -> TRANSIENT
//   - default -> FATAL

class AgentError extends Error {
  constructor(category, message, context = {}) {
    super(message);
    this.name = "AgentError";
    this.category = category;
    this.context = context;
    this.timestamp = new Date().toISOString();
    this.retryable = ["transient", "resource"].includes(category);
    // TODO: initialize additional fields as needed
  }
}

const ErrorCategory = {
  TRANSIENT: "transient",
  VALIDATION: "validation",
  RESOURCE: "resource",
  FATAL: "fatal"
};

const EscalationTrigger = {
  // TODO: define escalation rules per category
  // { maxRetries: number, escalateAfter: string }
};

function classifyError(error) {
  // TODO: implement status code -> category mapping
}

module.exports = { AgentError, ErrorCategory, EscalationTrigger, classifyError };
