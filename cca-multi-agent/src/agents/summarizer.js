const Anthropic = require("@anthropic-ai/sdk");

// TODO: Step 5 — Define summarizeTools schema
// Tool name: "summarize_document"
// Properties: summary (string, 2-3 sentences), actionItems (array), keyFigures (array)
// Required: summary
const summarizeTools = [
  // TODO: implement tool definition
];

// TODO: Implement runSummarizer(classifiedData, bus)
// 1. Create Anthropic client
// 2. Send classifiedData as JSON in user message
// 3. If stop_reason === "tool_use", publish to bus under "summarized" stage and return input
// 4. Throw if tool not used
async function runSummarizer(classifiedData, bus) {
  // TODO: implement
}

module.exports = { runSummarizer };
