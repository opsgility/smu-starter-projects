const Anthropic = require("@anthropic-ai/sdk");
const client = new Anthropic();

// TODO: Task 1 — Implement classifyWithPrefill(documentText)
// Use the prefill technique to guarantee JSON output format:
//   - Add a partial assistant message: { role: "assistant", content: '{"category":"' }
//   - Claude continues from this prefix, so output always starts as valid JSON
//   - Reconstruct the full JSON: '{"category":"' + response.content[0].text
//   - Parse and return the full JSON object
//
// System prompt: classify into invoice/contract/report/correspondence/technical_spec
// Respond with ONLY a JSON object — no text before or after

async function classifyWithPrefill(documentText) {
  // TODO: implement
}

// Test the prefill approach with sample documents
async function main() {
  const testDocs = [
    "INVOICE #001\nFrom: Acme Corp\nAmount: $5,200\nDue: Net 30",
    "This Non-Disclosure Agreement between NovaPulse and TechVentures...",
    "Q1 Engineering Velocity Report. Sprint completion: 91%.",
    "From: sarah@novapulse.com\nHey team, please review the auth migration plan."
  ];

  for (const doc of testDocs) {
    console.log(`\n--- Document ---`);
    console.log(doc.substring(0, 50) + "...");
    try {
      const result = await classifyWithPrefill(doc);
      console.log("Result:", JSON.stringify(result, null, 2));
    } catch (err) {
      console.error(`Error: ${err.message}`);
    }
  }
}

main().catch(console.error);
