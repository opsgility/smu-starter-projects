#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "multi-tool",
  version: "0.1.0",
});

// === Lesson 4 completed work — DO NOT MODIFY ===
server.registerTool(
  "greet",
  {
    title: "Greet",
    description: "Greet someone by name. Set formal=true for a more formal greeting.",
    inputSchema: {
      name: z.string().describe("The person's name"),
      formal: z.boolean().optional().describe("If true, use a formal greeting"),
    },
  },
  async ({ name, formal }) => ({
    content: [
      {
        type: "text",
        text: formal ? `Good day, ${name}.` : `Hello, ${name}!`,
      },
    ],
  }),
);

server.registerTool(
  "add_numbers",
  {
    title: "Add Numbers",
    description: "Return the sum of two numbers.",
    inputSchema: {
      a: z.number().describe("First number"),
      b: z.number().describe("Second number"),
    },
  },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a + b) }],
  }),
);

// === Lesson 6 work goes here ===

// TODO (Task 1): Register the `fetch_url` tool.
//   Input schema:
//     - url: string — must be HTTPS only (use Zod refinement)
//     - timeoutMs?: number — default 5000, max 30000
//   Output schema (use outputSchema for structured output):
//     - status: number
//     - headers: record of string -> string
//     - body: string (truncate to 10000 chars max)
//   Annotations: readOnlyHint=true, openWorldHint=true
//   On non-2xx response or fetch failure, return { isError: true, content: [...] }

// TODO (Task 2): Register the `format_json` tool.
//   Input schema:
//     - json: string — use .refine() to validate it parses as JSON
//     - indent?: 2 | 4 — default 2
//   Returns: pretty-printed string in content[0].text

// TODO (Task 3): Register the `calculate` tool.
//   Input schema (discriminated union):
//     { op: 'add' | 'subtract' | 'multiply' | 'divide', a: number, b: number }
//   Output schema:
//     - result: number
//     - expression: string (e.g., "12 + 8 = 20")
//   On divide-by-zero, return { isError: true, content: [...] }

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("multi-tool MCP server connected on stdio");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
