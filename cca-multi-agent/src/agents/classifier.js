const Anthropic = require("@anthropic-ai/sdk");

// TODO: Step 4 — Define classifyTools schema
// Tool name: "classify_document"
// Properties: category (enum), priority (enum: high/medium/low), confidence (0-1), tags (array)
// Required: category, priority, confidence
const classifyTools = [
  // TODO: implement tool definition
];

// TODO: Implement runClassifier(extractedData, bus)
// 1. Create Anthropic client
// 2. Send extractedData as JSON in user message
// 3. If stop_reason === "tool_use", publish to bus under "classified" stage and return input
// 4. Throw if tool not used
async function runClassifier(extractedData, bus) {
  // TODO: implement
}

module.exports = { runClassifier };
