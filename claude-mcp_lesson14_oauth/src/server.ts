#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express, { type Request, type Response } from "express";
import { randomUUID } from "node:crypto";
import { z } from "zod";
import { requireBearerToken } from "./middleware/bearerToken.js";

// === Lesson 14 transport configuration (carried over from Lesson 12) ===
const PORT = 3000;
const ALLOWED_ORIGINS = new Set<string>(["http://localhost", "http://127.0.0.1"]);
const RESOURCE_SERVER_URL =
  process.env.RESOURCE_SERVER_URL ?? `http://localhost:${PORT}/mcp`;
const EXPECTED_ISSUER = process.env.EXPECTED_ISSUER ?? "http://localhost:4000";

const server = new McpServer({
  name: "oauth-resource",
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

// === Streamable HTTP transport (completed in Lesson 12) ===

function originAllowlist(req: Request, res: Response, next: () => void): void {
  const origin = req.headers.origin;
  if (origin && !ALLOWED_ORIGINS.has(origin)) {
    res.status(403).json({ error: "origin_not_allowed", origin });
    return;
  }
  next();
}

async function main(): Promise<void> {
  const app = express();
  app.use(express.json());
  app.use(originAllowlist);

  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: () => randomUUID(),
  });
  await server.connect(transport);

  // === Lesson 14 work goes here ===
  //
  // TODO (Task 3): Serve the OAuth Protected Resource metadata document.
  //   Per RFC 9728, this tells clients which authorization servers can mint
  //   tokens for THIS resource and which auth methods to use.
  //
  //   Return JSON shaped like:
  //     {
  //       "resource": RESOURCE_SERVER_URL,
  //       "authorization_servers": [EXPECTED_ISSUER],
  //       "bearer_methods_supported": ["header"]
  //     }
  app.get("/.well-known/oauth-protected-resource", (_req, res) => {
    // TODO: replace this stub with the real metadata response described above.
    res.status(501).json({ error: "well_known_not_implemented" });
  });

  // TODO (Task 2): mount `requireBearerToken` middleware in front of the /mcp
  // route so every request must carry a valid JWT. Example:
  //
  //   app.all("/mcp", requireBearerToken, (req, res) =>
  //     transport.handleRequest(req, res, req.body),
  //   );
  //
  // For now the middleware is a stub returning 501 — wire it up after you
  // implement the four validation steps in src/middleware/bearerToken.ts.
  void requireBearerToken;

  app.all("/mcp", (req, res) => {
    void transport.handleRequest(req, res, req.body);
  });

  app.listen(PORT, "127.0.0.1", () => {
    console.error(
      `oauth-resource MCP server listening on http://127.0.0.1:${PORT}/mcp`,
    );
  });
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
