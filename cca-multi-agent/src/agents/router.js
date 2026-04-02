const Anthropic = require("@anthropic-ai/sdk");

// TODO: Step 6 — Define routeTools schema
// Tool name: "route_document"
// Properties: destination (enum: finance_team/legal_team/management/operations/archive),
//             urgency (enum: immediate/same_day/standard),
//             notifyParties (array), reason (string)
// Required: destination, urgency, reason
const routeTools = [
  // TODO: implement tool definition
];

// TODO: Implement runRouter(summarizedData, bus)
// 1. Create Anthropic client
// 2. Send summarizedData as JSON in user message
// 3. If stop_reason === "tool_use", publish to bus under "routed" stage and return input
// 4. Throw if tool not used
async function runRouter(summarizedData, bus) {
  // TODO: implement
}

module.exports = { runRouter };
