const { Errors, ErrorCategory } = require("./errors/error-types");
const { EscalationManager } = require("./escalation/triggers");
const { MonitoringDashboard } = require("./monitoring/dashboard");

// TODO: Task 4 — Implement simulate()
// Run 20 document processing scenarios that exercise all error types and escalation triggers
//
// Scenarios to include:
//   - "success" with high confidence (0.88-0.95) — happy path
//   - "low_confidence" (0.45) — triggers confidence threshold escalation
//   - "transient_error" — rate limit; three consecutive should trigger consecutive failure escalation
//   - "validation_error" — classification failed
//   - "fatal_error" — pipeline corruption; immediate escalation
//
// After all scenarios, call dashboard.printDashboard() and log escalation history

async function simulate() {
  const escalation = new EscalationManager({
    confidenceThreshold: 0.65,
    consecutiveFailureLimit: 3
  });
  const dashboard = new MonitoringDashboard();

  const scenarios = [
    { type: "success", confidence: 0.95 },
    { type: "success", confidence: 0.88 },
    { type: "low_confidence", confidence: 0.45 },  // confidence threshold trigger
    { type: "transient_error" },                     // consecutive failure #1
    { type: "transient_error" },                     // consecutive failure #2
    { type: "transient_error" },                     // consecutive failure #3 -> escalate
    { type: "success", confidence: 0.91 },           // resets consecutive count
    { type: "validation_error" },
    { type: "success", confidence: 0.82 },
    { type: "fatal_error" },                         // immediate escalation
    // TODO: add 10 more scenarios for a total of 20
  ];

  for (let i = 0; i < scenarios.length; i++) {
    const scenario = scenarios[i];
    const docId = i + 1;
    const startTime = Date.now();

    // Simulate processing delay
    await new Promise(r => setTimeout(r, 100 + Math.random() * 200));
    const latency = Date.now() - startTime;

    switch (scenario.type) {
      case "success": {
        dashboard.recordProcessing(docId, latency, true);
        escalation.recordSuccess("classifier");
        const esc = escalation.checkConfidenceThreshold(docId, scenario.confidence, "report");
        if (esc) {
          dashboard.recordEscalation(esc);
          console.log(`ESCALATION: ${esc.message}`);
        }
        break;
      }

      case "low_confidence": {
        dashboard.recordProcessing(docId, latency, true);
        const confEsc = escalation.checkConfidenceThreshold(docId, scenario.confidence, "contract");
        if (confEsc) {
          dashboard.recordEscalation(confEsc);
          console.log(`ESCALATION: ${confEsc.message}`);
        }
        break;
      }

      case "transient_error": {
        const error = Errors.rateLimited(5000);
        dashboard.recordProcessing(docId, latency, false, error);
        const failEsc = escalation.recordFailure("classifier", error);
        if (failEsc) {
          dashboard.recordEscalation(failEsc);
          console.log(`ESCALATION: ${failEsc.message}`);
        }
        break;
      }

      case "validation_error": {
        const error = Errors.classificationFailed(docId, "Invalid confidence score returned");
        dashboard.recordProcessing(docId, latency, false, error);
        break;
      }

      case "fatal_error": {
        const fatal = Errors.pipelineCorrupted("classifier", "Model returned empty response");
        dashboard.recordProcessing(docId, latency, false, fatal);
        dashboard.recordEscalation({
          trigger: "fatal_error",
          message: fatal.message,
          action: "halt_pipeline",
          timestamp: new Date().toISOString()
        });
        console.log(`FATAL: ${fatal.message}`);
        break;
      }
    }

    dashboard.recordComponentHealth(
      "classifier",
      scenario.type === "fatal_error" ? "down" : scenario.type.includes("error") ? "degraded" : "healthy",
      latency
    );
  }

  dashboard.printDashboard();

  console.log("\nEscalation History:");
  for (const esc of escalation.getHistory()) {
    console.log(`  [${esc.trigger}] ${esc.message}`);
  }
}

simulate().catch(console.error);
