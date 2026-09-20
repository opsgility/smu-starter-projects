// TODO: Task 3 — Define at least two prompt variants for A/B comparison
//
// Each variant: { name, system, examples }
// - examples: array of { role, content } message pairs for few-shot (or [] for zero-shot)
//
// Variant 1 (baseline/zero-shot): minimal system prompt, no examples
// Variant 2 (few-shot): detailed system prompt + 3 few-shot examples
// Optional Variant 3 (chain-of-thought): step-by-step reasoning prompt

const ZERO_SHOT = {
  name: "zero-shot",
  system: `Classify the following document into exactly one category: invoice, contract, report, correspondence, technical_spec.
Respond with JSON: {"category": "...", "confidence": 0.0-1.0, "reasoning": "..."}`,
  examples: []
};

const FEW_SHOT = {
  name: "few-shot",
  system: `You are a document classification specialist for DocStream, an enterprise document intelligence platform.
Classify documents into exactly one of these categories:
- invoice: Bills, payment requests, purchase orders, receipts
- contract: Legal agreements, NDAs, service level agreements, amendments
- report: Financial reports, status updates, meeting notes, postmortems
- correspondence: Emails, memos, letters, internal communications
- technical_spec: API docs, architecture documents, requirements specs

Respond with JSON: {"category": "...", "confidence": 0.0-1.0, "reasoning": "..."}
Rules: Never invent categories. Set confidence < 0.7 for ambiguous documents.`,
  examples: [
    // TODO: add 3 few-shot example pairs here
    // Each pair: { role: "user", content: "DOCUMENT: ..." }, { role: "assistant", content: '{"category":...}' }
  ]
};

// TODO: optional — add chain-of-thought variant

const PROMPT_VARIANTS = [ZERO_SHOT, FEW_SHOT];

module.exports = { PROMPT_VARIANTS, ZERO_SHOT, FEW_SHOT };
