const Anthropic = require("@anthropic-ai/sdk");
const client = new Anthropic();

// TODO: Task 2 — Implement extractFacts(chunk)
// Use Claude to extract all critical facts from a document chunk.
// Each fact should have: fact, category, confidence, quote (verbatim source)
//
// System prompt rules (critical):
//   - Never round numbers — $12,456.78 stays $12,456.78
//   - Never paraphrase dates — "March 15, 2026" stays "March 15, 2026"
//   - Never merge separate facts
//   - If contradictions found, extract BOTH and note the contradiction
//
// Use prefill technique: respond with "[" to force JSON array output
// After getting response, reconstruct: "[" + response.content[0].text
//
// Add provenance to each fact:
//   { ...fact, provenance: { chunk_index, start_offset, end_offset } }

async function extractFacts(chunk) {
  // TODO: implement
}

module.exports = { extractFacts };
