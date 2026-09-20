const Anthropic = require("@anthropic-ai/sdk");
const fs = require("fs");
const client = new Anthropic();

// TODO: Task 2 — Implement the batch processing pipeline with prefill
//
// prepareBatchRequests(documents): map each doc to a batch request
//   - custom_id: "doc-{i}-{doc.id}"
//   - params: model, max_tokens 500, system prompt, messages with prefill
//   - Include prefill: { role: "assistant", content: '{"category":"' }
//
// writeBatchFile(requests, filePath): write JSONL (one JSON per line)
//
// submitBatch(filePath): upload file + create batch, return batch object
//
// waitForBatch(batchId): poll every 10s until status === "ended" or "failed"
//
// getResults(batch): parse output file JSONL, reconstruct JSON with prefill prefix
//   - Return array of { custom_id, classification }
//
// compareCosts(documentCount, avgInputTokens, avgOutputTokens): log sync vs batch cost

// TODO: implement all functions above

async function prepareBatchRequests(documents) {
  // TODO: implement
}

function writeBatchFile(requests, filePath) {
  // TODO: implement
}

async function submitBatch(filePath) {
  // TODO: implement
}

async function waitForBatch(batchId) {
  // TODO: implement
}

async function getResults(batch) {
  // TODO: implement
}

function compareCosts(documentCount, avgInputTokens, avgOutputTokens) {
  // TODO: implement cost comparison calculation
}

async function main() {
  // Load test documents (at least 10)
  const documents = [
    { id: "doc_001", text: "INVOICE #2026-0501 from CloudScale Solutions. Amount: $47,500. Due: Net 30." },
    { id: "doc_002", text: "MEMORANDUM to Engineering Staff re: Q2 Architecture Review on April 15th." },
    { id: "doc_003", text: "Master Services Agreement between NovaPulse Technologies and DataFlow Inc..." },
    { id: "doc_004", text: "Q1 2026 Revenue Report. Revenue: $2.3M (+15% YoY). ARR: $9.2M." },
    { id: "doc_005", text: "Dear Mr. Chen, Thank you for your inquiry about our Enterprise tier pricing..." },
    // TODO: add 5+ more documents
  ];

  const requests = await prepareBatchRequests(documents);
  const batchFile = "batch-input.jsonl";
  writeBatchFile(requests, batchFile);

  const batch = await submitBatch(batchFile);
  const completedBatch = await waitForBatch(batch.id);
  const results = await getResults(completedBatch);

  console.log("\n=== Batch Results ===");
  for (const r of results) {
    console.log(`${r.custom_id}: ${JSON.stringify(r.classification)}`);
  }

  compareCosts(documents.length, 200, 80);
}

main().catch(console.error);
