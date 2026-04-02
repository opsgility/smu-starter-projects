// TODO: Step 2 — Implement the CircuitBreaker class
// States: CLOSED (normal), OPEN (using fallback), HALF_OPEN (testing recovery)
//
// constructor(options): failureThreshold (default 3), resetTimeoutMs (default 30000),
//                       halfOpenMaxAttempts (default 1)
//
// execute(fn, fallbackFn):
//   - OPEN: check if resetTimeoutMs elapsed -> transition to HALF_OPEN, else use fallback
//   - Try fn(); on success call onSuccess(), on failure call onFailure() + use fallback
//
// onSuccess(): increment successCount; if HALF_OPEN -> close circuit
// onFailure(error): increment failureCount; if >= threshold -> open circuit
// getStatus(): return { state, failureCount, successCount, totalCalls }

class CircuitBreaker {
  constructor(options = {}) {
    this.failureThreshold = options.failureThreshold || 3;
    this.resetTimeoutMs = options.resetTimeoutMs || 30000;
    this.halfOpenMaxAttempts = options.halfOpenMaxAttempts || 1;

    this.state = "CLOSED"; // CLOSED, OPEN, HALF_OPEN
    this.failureCount = 0;
    this.lastFailureTime = null;
    this.halfOpenAttempts = 0;
    this.successCount = 0;
    this.totalCalls = 0;
    // TODO: initialize additional state as needed
  }

  async execute(fn, fallbackFn) {
    // TODO: implement
  }

  onSuccess() {
    // TODO: implement
  }

  onFailure(error) {
    // TODO: implement
  }

  getStatus() {
    // TODO: implement
    return {
      state: this.state,
      failureCount: this.failureCount,
      successCount: this.successCount,
      totalCalls: this.totalCalls
    };
  }
}

module.exports = { CircuitBreaker };
