#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
// TODO (Task 1): swap stdio for Streamable HTTP — uncomment these imports.
// import express from "express";
// import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

// === Lesson 12 transport configuration ===
const PORT = 3000;
const ALLOWED_ORIGINS = new Set<string>(["http://localhost", "http://127.0.0.1"]);

const server = new McpServer({
  name: "streamable-http",
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

// === Lesson 12 work goes here ===
//
// You will swap the stdio transport for Streamable HTTP. Three steps:
//
//   1) Express app
//      - Build an Express app, parse JSON bodies, and add a small middleware
//        that rejects requests whose `Origin` header is not in ALLOWED_ORIGINS
//        with HTTP 403. This is your DNS-rebinding defense.
//
//   2) StreamableHTTPServerTransport with sessionIdGenerator
//      - Create a single StreamableHTTPServerTransport with a
//        `sessionIdGenerator` (e.g., `() => crypto.randomUUID()`).
//      - Mount POST/GET/DELETE on `/mcp` and route them all into
//        `transport.handleRequest(req, res, req.body)`.
//      - Call `await server.connect(transport)` once at startup.
//
//   3) Bind to 127.0.0.1 with the origin allowlist middleware
//      - `app.listen(PORT, "127.0.0.1", ...)` — do NOT bind to 0.0.0.0.
//      - Log "streamable-http MCP server listening on http://127.0.0.1:3000/mcp"
//        via console.error (never console.log on any MCP server).
//
// Until those three steps are wired, the server still runs on stdio so the
// starter compiles and starts out of the box. Replace `main()` below in
// Tasks 1 and 2.

async function main() {
  // TODO (Tasks 1 & 2): replace the stdio transport with Streamable HTTP.
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("streamable-http MCP server connected on stdio (replace in Tasks 1 & 2)");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
