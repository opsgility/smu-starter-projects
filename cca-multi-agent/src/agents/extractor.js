const Anthropic = require("@anthropic-ai/sdk");

// TODO: Step 3 — Define extractionTools schema
// Tool name: "extract_fields"
// Properties: title, date, parties (array), amounts (array of objects), keyTerms (array), rawLength
// Required: title, parties, keyTerms, rawLength
const extractionTools = [
  // TODO: implement tool definition
];

// TODO: Implement runExtractor(documentText, bus)
// 1. Create Anthropic client
// 2. Call messages.create() with extractionTools
// 3. If stop_reason === "tool_use", publish to bus under "extracted" stage and return input
// 4. Throw if tool not used
async function runExtractor(documentText, bus) {
  // TODO: implement
}

module.exports = { runExtractor };
