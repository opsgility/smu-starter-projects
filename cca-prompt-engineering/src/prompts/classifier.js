// TODO: Task 1 — Create a production-quality system prompt for the DocStream classifier
//
// The SYSTEM_PROMPT should include:
//   1. Role definition: document classification specialist for DocStream
//   2. Task specification: classify into exactly one of 5 categories:
//      invoice, contract, report, correspondence, technical_spec
//   3. Output format: JSON with category, confidence (0.0-1.0), and reasoning
//   4. Behavioral constraints:
//      - Never invent categories outside the five listed
//      - Choose primary purpose when document could fit multiple categories
//      - Set confidence below 0.7 for ambiguous documents
//      - Always explain reasoning, especially for edge cases

const SYSTEM_PROMPT = `You are a document classification specialist for DocStream, an enterprise document intelligence platform.

// TODO: complete the system prompt with:
//   - List of the 5 valid categories with descriptions
//   - Output format specification (JSON with category, confidence, reasoning)
//   - Behavioral rules
`;

module.exports = { SYSTEM_PROMPT };
