const Anthropic = require("@anthropic-ai/sdk");
const { CostTracker } = require("./cost-tracker");

// Shared tracker with $0.50 budget for testing
const tracker = new CostTracker(0.50);

// TODO: Step 2 — Implement trackedCreate(agentName, params)
// 1. Create Anthropic client
// 2. Call client.messages.create(params)
// 3. Record usage: tracker.record(agentName, params.model, response.usage)
// 4. Return the response
async function trackedCreate(agentName, params) {
  // TODO: implement
}

// TODO: Run a 4-agent pipeline with cost tracking
// Agent 1 (extractor): claude-sonnet-4-20250514 — extract fields from invoice
// Agent 2 (classifier): claude-sonnet-4-20250514 — classify the extracted fields
// Agent 3 (summarizer): claude-haiku-35-20241022 — one-sentence summary (cheaper model)
// Agent 4 (router): claude-haiku-35-20241022 — route to department (simpler task)
// Print cost report and optimization notes at the end
async function main() {
  console.log("=== DocStream Cost-Tracked Pipeline ===\n");

  // TODO: implement 4-agent pipeline calls and print cost report
}

main().catch(console.error);
