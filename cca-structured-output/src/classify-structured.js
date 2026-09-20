const Anthropic = require("@anthropic-ai/sdk");
const { CLASSIFY_TOOL } = require("./schemas/classify-schema");

const client = new Anthropic();

// TODO: Task 2 — Implement classifyWithToolUse(documentText)
// 1. Call client.messages.create() with:
//    - model: "claude-sonnet-4-20250514"
//    - max_tokens: 1024
//    - system: document classification specialist prompt
//    - tools: [CLASSIFY_TOOL]
//    - tool_choice: { type: "tool", name: "classify_document" }  <-- forces tool use
//    - messages: [{ role: "user", content: `Classify this document:\n\n${documentText}` }]
// 2. Find the tool_use block in response.content
// 3. Throw if tool not used
// 4. Return toolUse.input (guaranteed to match schema)

async function classifyWithToolUse(documentText) {
  // TODO: implement
}

// Test against sample documents and verify schema conformance
async function main() {
  const testDocs = [
    "INVOICE #2024-0501\nFrom: CloudScale Solutions\nTo: NovaPulse Technologies\nAmount: $47,500\nDue: Net 30",
    "This Master Services Agreement is entered into between NovaPulse Technologies and DataFlow Inc...",
    "Q1 2024 Engineering Velocity Report. Sprint completion: 87%. Blocked items: 3.",
    "Hey team — can you sync on the auth service migration plan before Friday?"
  ];

  for (const doc of testDocs) {
    console.log(`\n--- Document ---`);
    console.log(doc.substring(0, 60) + "...");
    try {
      const result = await classifyWithToolUse(doc);
      console.log("Classification:", JSON.stringify(result, null, 2));
    } catch (err) {
      console.error(`Error: ${err.message}`);
    }
  }
}

main().catch(console.error);
