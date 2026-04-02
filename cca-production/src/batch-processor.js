const Anthropic = require("@anthropic-ai/sdk");
const { documents } = require("./documents");

const client = new Anthropic();

// TODO: Step 3 — Implement buildBatchRequests(docs)
// Map each document to a batch request object:
//   { custom_id: doc.id, params: { model, max_tokens, system, messages } }
// System prompt: classify document as JSON with category, confidence, reasoning
// Note: use custom_id to map results back to documents later
function buildBatchRequests(docs) {
  // TODO: implement
  return docs.map(doc => ({
    custom_id: doc.id,
    params: {
      model: "claude-sonnet-4-20250514",
      max_tokens: 512,
      system: "You are a document classifier. Respond with a JSON object containing: category (invoice|contract|report|memo|legal_filing|correspondence), confidence (0-1), and a one-sentence reasoning. Respond ONLY with the JSON object, no other text.",
      messages: [
        { role: "user", content: `Classify this document:\n\n${doc.text}` }
      ]
    }
  }));
}

// TODO: Step 3 — Implement submitBatch()
// 1. Build requests from documents
// 2. Call client.messages.batches.create({ requests })
// 3. Log batch ID and status
// 4. Return { batchId, startTime }
async function submitBatch() {
  // TODO: implement
}

// TODO: Step 4 — Implement waitForBatch(batchId)
// Poll client.messages.batches.retrieve(batchId) every 5 seconds
// Log progress: status and percentage complete
// Return when processing_status === "ended"
async function waitForBatch(batchId) {
  // TODO: implement
}

// TODO: Step 5 — Implement getResults(batchId)
// Iterate client.messages.batches.results(batchId)
// For succeeded results: parse JSON text content, handle parse errors
// For failed results: record the error
// Return array of { docId, status, classification } or { docId, status, error }
async function getResults(batchId) {
  // TODO: implement
}

// TODO: Step 6 — Implement main()
// Call submitBatch(), waitForBatch(), getResults()
// Print results table and summary
async function main() {
  // TODO: implement
}

main().catch(console.error);
