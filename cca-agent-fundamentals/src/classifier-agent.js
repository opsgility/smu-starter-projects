const Anthropic = require("@anthropic-ai/sdk");

// TODO: Step 2 — Define the classification tool schema
// The tool should have a name, description, and input_schema with:
//   - category (string, enum of 6 document types)
//   - confidence (number, 0-1)
//   - reasoning (string)
const tools = [
  // TODO: implement tool definition
];

// TODO: Step 3 — Implement the core agent loop
// The function should:
//   1. Create an Anthropic client
//   2. Build an initial messages array with the document text
//   3. Loop while stop_reason === "tool_use"
//   4. Execute the tool (acknowledge the classification)
//   5. Append the tool result and continue the loop
//   6. Return the final text response and messages
async function classifyDocument(documentText) {
  // TODO: implement
}

// TODO: Step 4 — Add test documents and a main() runner
const testDocuments = [
  // TODO: add 3 test documents (invoice, memo, contract)
];

async function main() {
  // TODO: iterate over testDocuments and call classifyDocument()
}

main().catch(console.error);
