const Anthropic = require("@anthropic-ai/sdk");
const { SYSTEM_PROMPT } = require("./prompts/classifier");
const { FEW_SHOT_EXAMPLES } = require("./prompts/few-shot-examples");

const client = new Anthropic();

// TODO: Task 3 — Implement classifyDocument(documentText)
// Combines SYSTEM_PROMPT and FEW_SHOT_EXAMPLES for a production classifier
// 1. Call client.messages.create() with:
//    - model: "claude-sonnet-4-20250514"
//    - max_tokens: 300
//    - system: SYSTEM_PROMPT
//    - messages: [...FEW_SHOT_EXAMPLES, { role: "user", content: `DOCUMENT: ${documentText}` }]
// 2. Parse and return the JSON response
async function classifyDocument(documentText) {
  // TODO: implement
}

// Run classifier against test documents
async function main() {
  const { TEST_DOCUMENTS } = require("./test-documents");

  for (const doc of TEST_DOCUMENTS) {
    console.log(`\n--- ${doc.name} ---`);
    try {
      const result = await classifyDocument(doc.text);
      console.log(JSON.stringify(result, null, 2));
    } catch (err) {
      console.error(`Error: ${err.message}`);
    }
  }
}

main().catch(console.error);
