// TODO: Task 2 — Create few-shot examples that demonstrate correct classification
//
// FEW_SHOT_EXAMPLES should be an array of { role, content } message pairs
// Include at least 3 examples:
//   1. A clear-cut invoice (easy case)
//   2. A contract that contains financial terms (edge case: could be confused with invoice)
//   3. A technical email about architecture (edge case: correspondence vs technical_spec)
//
// Each assistant response should be a JSON string with category, confidence, and reasoning
// The reasoning for edge cases must explain WHY one category was chosen over another

const FEW_SHOT_EXAMPLES = [
  // Example 1: Clear invoice
  {
    role: "user",
    content: "DOCUMENT: Payment Request #4521\nFrom: Acme Corp\nAmount Due: $12,450.00\nDue Date: 2026-04-15\nItems: Cloud hosting services (March 2026)\nPayment Terms: Net 30"
  },
  {
    role: "assistant",
    content: JSON.stringify({
      category: "invoice",
      confidence: 0.95,
      reasoning: "TODO: add reasoning"
    })
  },
  // TODO: add example 2 (contract with financial terms)
  // TODO: add example 3 (technical email — correspondence vs technical_spec)
];

module.exports = { FEW_SHOT_EXAMPLES };
