const Anthropic = require("@anthropic-ai/sdk");

// TODO: Step 1 — Implement retry wrapper with exponential backoff
// Retry on status 429, 529, and >= 500
// Use BASE_DELAY_MS * 2^(attempt-1) for delay
const MAX_RETRIES = 3;
const BASE_DELAY_MS = 1000;

async function callWithRetry(apiCallFn) {
  // TODO: implement retry loop
}

// TODO: Step 2 — Implement tool input validation
// Validate: category (must be in enum), confidence (0-1 number), reasoning (>= 10 chars)
// Return { valid: boolean, errors: string[] }
function validateClassification(input) {
  // TODO: implement
}

// TODO: Step 3 — Implement tool result formatter
// On validation failure: return tool_result with is_error: true and error message
// On success: return tool_result with classification, timestamp, status: "accepted"
function formatToolResult(toolUseId, input) {
  // TODO: implement
}

// TODO: Step 4 — Build the resilient agent loop
// Max 10 iterations guard, uses callWithRetry() and formatToolResult()
// Return { success: boolean, finalText, iterations } or { success: false, error, iterations }
const MAX_ITERATIONS = 10;

async function classifyDocumentResilient(documentText) {
  // TODO: implement
}

// TODO: Step 5 — Test with edge cases
async function main() {
  const testCases = [
    { name: "Normal invoice", text: "INVOICE #001\nAmount: $500\nDue: Net 30\nServices: Consulting" },
    { name: "Ambiguous document", text: "Hey team, attached is the Q3 data. Let me know if the numbers look right." },
    { name: "Empty document", text: "" },
    { name: "Non-English", text: "Factura #2024-001\nMonto: $1,500.00\nServicios: Consultoría técnica" }
  ];

  // TODO: iterate testCases and call classifyDocumentResilient()
}

main().catch(console.error);
