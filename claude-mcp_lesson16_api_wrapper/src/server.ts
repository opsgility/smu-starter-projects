#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express, { type Request, type Response, type NextFunction } from "express";
import { randomUUID } from "node:crypto";
import { AsyncLocalStorage } from "node:async_hooks";
import { z } from "zod";
import { bearerTokenMiddleware } from "./middleware/bearerToken.js";

// === Lesson 16 configuration ===
const PORT = Number(process.env.PORT ?? 3000);
const RESOURCE_URL = process.env.RESOURCE_URL ?? `http://127.0.0.1:${PORT}/mcp`;
const OAUTH_ISSUER = process.env.OAUTH_ISSUER ?? "http://127.0.0.1:4000";
const OAUTH_AUDIENCE = process.env.OAUTH_AUDIENCE ?? RESOURCE_URL;
const OAUTH_JWKS_URI = process.env.OAUTH_JWKS_URI ?? `${OAUTH_ISSUER}/.well-known/jwks.json`;
const ALLOWED_ORIGINS = new Set<string>([
  "http://localhost",
  "http://127.0.0.1",
  `http://localhost:${PORT}`,
  `http://127.0.0.1:${PORT}`,
]);

// === AsyncLocalStorage for per-request caller context ===
// The bearer-token middleware decodes the JWT and runs each request inside this
// context so any tool handler can call getCallerContext() to access the caller's
// validated identity, tenant, scopes, and the raw bearer token (used for token
// forwarding when calling upstream APIs on the user's behalf).
export interface CallerContext {
  sub: string;
  tenantId?: string;
  scopes: string[];
  bearerToken: string;
}

export const callerContext = new AsyncLocalStorage<CallerContext>();

export function getCallerContext(): CallerContext {
  const ctx = callerContext.getStore();
  if (!ctx) throw new Error("missing caller context — tool called outside an authenticated request?");
  return ctx;
}

const server = new McpServer({
  name: "api-wrapper",
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

// === Lesson 16 work goes here =================================================
//
// You have FOUR new tools to implement. The bearer-token middleware below already
// validates the JWT and populates the callerContext for you, so every tool
// handler can call `getCallerContext()` to get { sub, tenantId, scopes, bearerToken }.
//
// Per-user scoping is the central theme: every database/REST call must be
// constrained by `ctx.sub`, and every cache key must include `ctx.sub` so two
// users never share cached entries. Skipping these is a multi-tenancy leak.

// TODO (Task 2): Register `search_shipments`.
//   Input schema:
//     - query: string (the search term)
//     - status?: enum ["pending", "in_transit", "delivered", "delayed"]
//     - limit?: number (1..50, default 10)
//     - cursor?: string (opaque pagination cursor)
//   Output schema:
//     - items: array of { id: string, query_match: string, status: string, owner_sub: string }
//     - nextCursor?: string
//   Annotations: readOnlyHint: true
//
//   Implementation requirements:
//     1. Read ctx = getCallerContext().
//     2. Build URL: `${MOCK_API_BASE}/shipments?query=...&status=...&limit=...&cursor=...`.
//     3. FORWARD ctx.bearerToken in the Authorization header so the upstream API
//        can apply its own access control. Mock API returns only the shipments
//        owned by the JWT subject.
//     4. The mock API already filters by sub — you should ALSO defensively check
//        that every returned item's owner_sub === ctx.sub before yielding it.
//     5. Run the upstream call through the LRU cache (see Task 4) keyed by
//        `${ctx.sub}:${query}:${status ?? ""}:${limit ?? 10}:${cursor ?? ""}`.

// TODO (Task 3): Register `get_shipment_history`.
//   Input schema:
//     - id: string (shipment id, e.g., "SHIP-0001")
//   Output schema:
//     - events: array of { ts: string, event: string }
//
//   Implementation requirements:
//     1. Open SQLite DB at process.env.SQLITE_PATH (use better-sqlite3).
//     2. Run a PARAMETERIZED query — never string-concatenate user input:
//          SELECT ts, event FROM shipments_history
//          WHERE shipment_id = ? AND owner_sub = ?
//          ORDER BY ts DESC LIMIT 50
//     3. Pass [id, ctx.sub] as parameters. The owner_sub filter is what stops
//        user A from reading user B's history even if they guess B's shipment id.
//     4. If the query returns zero rows, return { isError: true, content: [...] }
//        with a clean "shipment not found or not yours" message — don't leak
//        the difference between "doesn't exist" and "exists but isn't yours".

// TODO (Task 5): Register `record_delivery`.
//   Input schema:
//     - id: string (shipment id)
//     - signature: string (recipient signature, 1..200 chars)
//   Output schema:
//     - id: string
//     - delivered_at: string (ISO 8601)
//   Annotations: destructiveHint: false, idempotentHint: true
//
//   Implementation requirements:
//     1. Read ctx = getCallerContext().
//     2. REQUIRE scope: if (!ctx.scopes.includes("shipments:write")) return
//        { isError: true, content: [{ type: "text", text: "Missing scope: shipments:write" }] }.
//        The LLM can surface this to the user and ask them to re-auth with the
//        broader scope.
//     3. POST to `${MOCK_API_BASE}/shipments/${id}/deliveries` with the bearer
//        token forwarded and a JSON body { signature }.
//     4. Return the structured response { id, delivered_at } from the upstream.

// TODO (Task 4): Register `cache_stats`.
//   Input schema: {} (no args)
//   Output schema:
//     - hits: number
//     - misses: number
//     - hit_rate: number (0..1)
//     - per_user_keys: number (count of cache entries owned by the current user)
//
//   Implementation requirements:
//     - Implement an LRU cache (lru-cache package) with TTL of 5 minutes.
//     - Track hits/misses on every get.
//     - Cache keys MUST be prefixed with `${ctx.sub}:` so users never share
//       cache entries. `per_user_keys` reports only entries starting with
//       `${ctx.sub}:`.

// === Express + Streamable HTTP transport (already wired) ======================

async function main() {
  const app = express();
  app.use(express.json({ limit: "1mb" }));

  // Origin allowlist — DNS rebinding defense.
  app.use((req: Request, res: Response, next: NextFunction) => {
    const origin = req.headers.origin;
    if (origin && !ALLOWED_ORIGINS.has(origin)) {
      res.status(403).json({ error: "origin not allowed" });
      return;
    }
    next();
  });

  // .well-known/oauth-protected-resource — describes our auth requirements
  // so Claude Code's MCP client can discover the authorization server.
  app.get("/.well-known/oauth-protected-resource", (_req, res) => {
    res.json({
      resource: RESOURCE_URL,
      authorization_servers: [OAUTH_ISSUER],
      bearer_methods_supported: ["header"],
      scopes_supported: ["mcp:tools", "shipments:read", "shipments:write"],
    });
  });

  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: () => randomUUID(),
  });
  await server.connect(transport);

  // Bearer-token middleware sits in front of /mcp ONLY — the .well-known route
  // above is unauthenticated by design. The middleware validates the JWT and
  // wraps the rest of the request lifecycle in callerContext.run(...).
  const auth = bearerTokenMiddleware({
    jwksUri: OAUTH_JWKS_URI,
    issuer: OAUTH_ISSUER,
    audience: OAUTH_AUDIENCE,
  });

  const handle = async (req: Request, res: Response) => {
    await transport.handleRequest(req, res, req.body);
  };

  app.post("/mcp", auth, handle);
  app.get("/mcp", auth, handle);
  app.delete("/mcp", auth, handle);

  app.listen(PORT, "127.0.0.1", () => {
    console.error(`api-wrapper MCP server listening on http://127.0.0.1:${PORT}/mcp`);
    console.error(`OAuth issuer: ${OAUTH_ISSUER}`);
    console.error(`Audience:     ${OAUTH_AUDIENCE}`);
  });
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
