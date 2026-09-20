const Anthropic = require("@anthropic-ai/sdk");
const { CLASSIFY_TOOL } = require("./schemas/classify-schema");
const { validateStructure, validateSemantics, validateBusinessRules } = require("./validation/validators");

const client = new Anthropic();
const MAX_RETRIES = 3;

// TODO: Task 2 — Implement classifyWithRetry(documentText)
// Loop up to MAX_RETRIES times:
//   1. Call client.messages.create() with tool_choice forced
//   2. Find toolUse block; if missing, append a correction message and retry
//   3. Run all 3 validators on toolUse.input
//   4. If no errors: return { result, attempts }
//   5. If errors and retries remain: append tool_result with is_error content listing errors
//   6. If max retries exhausted: return { result, attempts, errors }
//
// Key pattern: when returning errors, use:
//   { role: "user", content: [{ type: "tool_result", tool_use_id, content: "Validation failed:\n..." }] }

async function classifyWithRetry(documentText) {
  let messages = [
    { role: "user", content: `Classify this document:\n\n${documentText}` }
  ];

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    console.log(`  Attempt ${attempt}/${MAX_RETRIES}...`);

    // TODO: implement the retry loop

  }
}

// Test with adversarial documents
async function main() {
  const adversarialDocs = [
    { name: "Minimal content", text: "FYI" },
    { name: "Mixed signals", text: "INVOICE: Legal Services Agreement. This contract establishes payment terms of $5,000/month for ongoing legal consultation. Signed by both parties on 2026-03-01." },
    { name: "Foreign language", text: "Rechnung Nr. 2026-0891. Betrag: EUR 4.500,00. Zahlungsziel: 30 Tage netto." }
  ];

  for (const doc of adversarialDocs) {
    console.log(`\n=== ${doc.name} ===`);
    try {
      const result = await classifyWithRetry(doc.text);
      console.log(`Result (${result.attempts} attempts):`, JSON.stringify(result.result, null, 2));
      if (result.errors) console.log("Remaining errors:", result.errors);
    } catch (err) {
      console.error(`Failed: ${err.message}`);
    }
  }
}

main().catch(console.error);
