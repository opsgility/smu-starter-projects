#!/usr/bin/env node
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = resolve(__dirname, "..", "data");

const server = new McpServer({
  name: "resources-prompts",
  version: "0.1.0",
});

// === Lessons 4 & 6 completed work — DO NOT MODIFY ===

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
    content: [{ type: "text", text: formal ? `Good day, ${name}.` : `Hello, ${name}!` }],
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
  async ({ a, b }) => ({ content: [{ type: "text", text: String(a + b) }] }),
);

server.registerTool(
  "fetch_url",
  {
    title: "Fetch URL",
    description: "Fetch an HTTPS URL and return status, headers, and body. HTTPS only.",
    inputSchema: {
      url: z.string().refine((u) => u.startsWith("https://"), "URL must use https://"),
      timeoutMs: z.number().int().min(1).max(30000).default(5000).optional(),
    },
    outputSchema: {
      status: z.number(),
      headers: z.record(z.string()),
      body: z.string(),
    },
    annotations: { readOnlyHint: true, openWorldHint: true },
  },
  async ({ url, timeoutMs }) => {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs ?? 5000);
    try {
      const res = await fetch(url, { signal: controller.signal });
      const headers: Record<string, string> = {};
      res.headers.forEach((v, k) => (headers[k] = v));
      const text = await res.text();
      const body = text.length > 10000 ? text.slice(0, 10000) + "...[truncated]" : text;
      const structured = { status: res.status, headers, body };
      return {
        content: [{ type: "text", text: JSON.stringify(structured, null, 2) }],
        structuredContent: structured,
        isError: !res.ok,
      };
    } catch (err) {
      return {
        content: [{ type: "text", text: `fetch_url failed: ${(err as Error).message}` }],
        isError: true,
      };
    } finally {
      clearTimeout(timer);
    }
  },
);

server.registerTool(
  "format_json",
  {
    title: "Format JSON",
    description: "Pretty-print a JSON string with 2 or 4 space indent.",
    inputSchema: {
      json: z.string().refine((s) => {
        try {
          JSON.parse(s);
          return true;
        } catch {
          return false;
        }
      }, "input must be valid JSON"),
      indent: z.union([z.literal(2), z.literal(4)]).default(2).optional(),
    },
  },
  async ({ json, indent }) => ({
    content: [{ type: "text", text: JSON.stringify(JSON.parse(json), null, indent ?? 2) }],
  }),
);

server.registerTool(
  "calculate",
  {
    title: "Calculate",
    description: "Perform a basic arithmetic operation on two numbers.",
    inputSchema: {
      op: z.enum(["add", "subtract", "multiply", "divide"]),
      a: z.number(),
      b: z.number(),
    },
    outputSchema: {
      result: z.number(),
      expression: z.string(),
    },
  },
  async ({ op, a, b }) => {
    if (op === "divide" && b === 0) {
      return {
        content: [{ type: "text", text: "Cannot divide by zero." }],
        isError: true,
      };
    }
    const result = op === "add" ? a + b : op === "subtract" ? a - b : op === "multiply" ? a * b : a / b;
    const sym = op === "add" ? "+" : op === "subtract" ? "-" : op === "multiply" ? "*" : "/";
    const structured = { result, expression: `${a} ${sym} ${b} = ${result}` };
    return {
      content: [{ type: "text", text: structured.expression }],
      structuredContent: structured,
    };
  },
);

// === Lesson 8 work goes here ===

// TODO (Task 1): Register a STATIC resource at uri "playbook://outage" that reads
//   data/playbooks/outage.md and returns it as text/markdown.
//
//   server.registerResource(
//     "outage-playbook",
//     "playbook://outage",
//     { title: "...", description: "...", mimeType: "text/markdown" },
//     async (uri) => ({ contents: [{ uri: uri.href, mimeType: "text/markdown", text: await readFile(...) }] })
//   );

// TODO (Task 2): Register a TEMPLATED resource at uri "wiki://{slug}" that reads
//   data/wiki/{slug}.md from disk. Return text/markdown. Handle missing files
//   by throwing — the SDK will surface a clean JSON-RPC error.
//
//   const tmpl = new ResourceTemplate("wiki://{slug}", { list: undefined });
//   server.registerResource("wiki", tmpl, { ... }, async (uri, { slug }) => { ... });

// TODO (Task 3): Register a PROMPT named "incident-triage" with arguments:
//     - severity: enum ["low", "med", "high", "critical"]
//     - service: string
//   Return a 2-message conversation:
//     1) system message with brief triage rules
//     2) user message instantiated with the args
//
//   server.registerPrompt(
//     "incident-triage",
//     { title: "...", description: "...", argsSchema: { severity: ..., service: ... } },
//     ({ severity, service }) => ({
//       messages: [
//         { role: "user", content: { type: "text", text: "..." } }
//       ]
//     })
//   );

// TODO (Task 6 — bonus): When a new wiki file appears under data/wiki/, send
//   a notifications/resources/list_changed notification so Claude Code refreshes
//   its @-autocomplete dynamically. Hint: use fs.watch on DATA_DIR/wiki and
//   call server.server.sendResourceListChanged().

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("resources-prompts MCP server connected on stdio");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});

// Re-export readFile to silence the unused-import warning until students wire it up.
export { readFile };
