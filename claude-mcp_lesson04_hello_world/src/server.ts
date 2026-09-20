#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "greeter",
  version: "0.1.0",
});

// TODO (Task 2): Register the `greet` tool.
//   - Input schema: { name: string, formal?: boolean }
//   - When formal === true, return "Good day, {name}."
//   - Otherwise return "Hello, {name}!"
//   - Use server.registerTool with a clear description and Zod input schema.
//
// Reference: https://github.com/modelcontextprotocol/typescript-sdk/blob/main/docs/server.md
//
// server.registerTool(
//   "greet",
//   {
//     description: "...",
//     inputSchema: { ... }
//   },
//   async ({ name, formal }) => ({ content: [{ type: "text", text: ... }] })
// );

// TODO (Bonus, Task 6): Register the `add_numbers` tool.
//   - Input schema: { a: number, b: number }
//   - Returns the sum as text.

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  // IMPORTANT: never use console.log in stdio MCP servers — it corrupts JSON-RPC frames on stdout.
  // Use console.error (stderr) for any diagnostic output.
  console.error("greeter MCP server connected on stdio");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
