const { AgentError, ErrorCategory } = require("./error-types");
const { ErrorChain } = require("./error-chain");

// Shared error chain for the pipeline run
const errorChain = new ErrorChain();

// TODO: Step 3 — Implement three simulated agents that can fail
//
// extractorAgent(doc): throw VALIDATION error if doc.length < 10
// classifierAgent(extracted): 40% chance of TRANSIENT "API timeout" error
// summarizerAgent(classified): throw VALIDATION error if classified.confidence < 0.5

async function extractorAgent(doc) {
  // TODO: implement with validation error
}

async function classifierAgent(extracted) {
  // TODO: implement with intermittent transient error
}

async function summarizerAgent(classified) {
  // TODO: implement with confidence validation
}

// TODO: Implement runAgentWithRetry(name, fn, input, maxRetries = 3)
// - Try fn(input) up to maxRetries times
// - On error: call errorChain.record(name, error)
//   - If shouldEscalate: return null
//   - If retryable and attempts remain: retry
//   - If not retryable: return null
// - Return null if all retries exhausted

async function runAgentWithRetry(name, fn, input, maxRetries = 3) {
  // TODO: implement
}

async function main() {
  const testDocs = [
    "INVOICE #2024-001 - NovaPulse Technologies - Amount: $15,000 - Due: April 15, 2024",
    "Short",
    "CONTRACT between Party A and Party B for services rendered in Q1 2024, total value $50,000"
  ];

  for (const doc of testDocs) {
    console.log(`\n${"=".repeat(50)}`);
    console.log(`Processing: "${doc.slice(0, 40)}..."`);

    const extracted = await runAgentWithRetry("extractor", extractorAgent, doc);
    if (!extracted) { console.log("Pipeline stopped at extraction"); continue; }

    const classified = await runAgentWithRetry("classifier", classifierAgent, extracted);
    if (!classified) { console.log("Pipeline stopped at classification"); continue; }

    const summarized = await runAgentWithRetry("summarizer", summarizerAgent, classified);
    if (!summarized) { console.log("Pipeline stopped at summarization"); continue; }

    console.log("Pipeline complete:", JSON.stringify(summarized));
  }

  console.log("\n=== Error Report ===");
  console.log(JSON.stringify(errorChain.getReport(), null, 2));
}

main().catch(console.error);
