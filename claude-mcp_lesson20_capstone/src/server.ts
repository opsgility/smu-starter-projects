#!/usr/bin/env node
/*
 * Lesson 20 Capstone — MCP Server Scaffold
 * =========================================
 *
 * Pick ONE track and build a production-quality MCP server. Delete the other
 * two `src/track-*` folders when you commit.
 *
 *  Track | Domain                               | Required Capabilities
 *  ------|--------------------------------------|----------------------------------------------------------------
 *   A    | DevOps — Kubernetes (read-only)      | Tools (list pods, describe deployment, get logs),
 *        |                                      | Resources (manifest YAMLs), Roots enforcement, structured output
 *   B    | Knowledge — Notion/Confluence wiki   | Tools (search, read), Resource templates with URI scheme,
 *        |                                      | Prompts (doc-writing template), Elicitation for confirmation
 *   C    | Data — Read-only Postgres analytics  | Tools (run SELECT with row caps), Resources (schema introspection),
 *        |                                      | OAuth 2.1, sampling for query summarization
 *
 * Required deliverables for ALL tracks (full list in README.md):
 *   1. Zod inputSchema AND outputSchema on every tool.
 *   2. At least one tool, one resource, and one prompt.
 *   3. console.error-only logging + notifications/message for user-visible logs.
 *   4. Streamable HTTP + OAuth 2.1 (Tracks B & C) OR stdio + Roots (Track A).
 *   5. MCP Inspector trace, README, manifest.json, server.json, 3+ vitest tests, demo.
 *
 * Track A keeps the StdioServerTransport below.
 * Tracks B and C should swap to StreamableHTTPServerTransport (see Lesson 12 starter).
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
// import { z } from "zod";

const server = new McpServer({
  name: "capstone",
  version: "0.1.0",
});

// === Capstone work goes here — pick your track ===

// TODO (Tool): register at least one tool with BOTH inputSchema and outputSchema.
//
// Example skeleton (uncomment and customize):
//
// server.registerTool(
//   "your_tool_name",
//   {
//     title: "Your Tool",
//     description: "Describe precisely what the tool does and when to use it.",
//     inputSchema: {
//       /* z.string(), z.number(), etc. */
//     },
//     outputSchema: {
//       /* structured fields the LLM can rely on */
//     },
//   },
//   async (args) => ({
//     structuredContent: { /* ... */ },
//     content: [{ type: "text", text: "..." }],
//   }),
// );

// TODO (Resource): register at least one static resource OR resource template.
//
// Example skeleton (uncomment and customize):
//
// server.registerResource(
//   "your_resource_name",
//   "your-scheme://identifier",
//   {
//     title: "Your Resource",
//     description: "Describe what consumers of this resource get.",
//     mimeType: "text/markdown",
//   },
//   async (uri) => ({
//     contents: [{ uri: uri.href, mimeType: "text/markdown", text: "..." }],
//   }),
// );

// TODO (Prompt): register at least one prompt template.
//
// Example skeleton (uncomment and customize):
//
// server.registerPrompt(
//   "your_prompt_name",
//   {
//     title: "Your Prompt",
//     description: "Describe what the prompt produces.",
//     argsSchema: {
//       /* z.string() etc. */
//     },
//   },
//   async (args) => ({
//     messages: [
//       { role: "user", content: { type: "text", text: "..." } },
//     ],
//   }),
// );

async function main() {
  // Track A: keep StdioServerTransport. Tracks B/C: swap for Streamable HTTP.
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("capstone MCP server connected on stdio");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
