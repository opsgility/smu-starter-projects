#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import express, { type Request, type Response, type NextFunction } from "express";
import { randomUUID } from "node:crypto";
import { AsyncLocalStorage } from "node:async_hooks";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { LRUCache } from "lru-cache";
import Database from "better-sqlite3";
import { z } from "zod";
import { bearerTokenMiddleware } from "./middleware/bearerToken.js";

// =============================================================================
// LESSON 18 — student work goes in main() and at the marked TODO sites below.
//
// TODO (Task 1): Replace this `logger` stub with a real pino instance.
//                Use LOG_LEVEL from env. Stream JSON lines to stderr only —
//                never stdout, even though this is HTTP transport, because the
//                same code may run under stdio in a derivative project.
//
// For now, only error/warn methods are routed to console.error so we never
// accidentally emit a console.log call. DO NOT extend this stub with .log /
// .info — students will replace it with pino in Task 1.
// =============================================================================
export const logger = {
  error: (...args: unknown[]) => console.error("[error]", ...args),
  warn: (...args: unknown[]) => console.error("[warn]", ...args),
  info: (...args: unknown[]) => console.error("[info]", ...args),
  debug: (...args: unknown[]) => console.error("[debug]", ...args),
};

// === Configuration ===
const PORT = Number(process.env.PORT ?? 3000);
const RESOURCE_URL = process.env.RESOURCE_URL ?? `http://127.0.0.1:${PORT}/mcp`;
const OAUTH_ISSUER = process.env.OAUTH_ISSUER ?? "http://127.0.0.1:4000";
const OAUTH_AUDIENCE = process.env.OAUTH_AUDIENCE ?? RESOURCE_URL;
const OAUTH_JWKS_URI = process.env.OAUTH_JWKS_URI ?? `${OAUTH_ISSUER}/.well-known/jwks.json`;
const MOCK_API_BASE = process.env.MOCK_API_BASE ?? "http://localhost:5000";
const SQLITE_PATH =
  process.env.SQLITE_PATH ?? resolve(dirname(fileURLToPath(import.meta.url)), "..", "..", "data", "shipments.db");
const ALLOWED_ORIGINS = new Set<string>([
  "http://localhost",
  "http://127.0.0.1",
  `http://localhost:${PORT}`,
  `http://127.0.0.1:${PORT}`,
]);

// === AsyncLocalStorage for caller context ===
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

// === LRU + TTL cache, keyed by `${sub}:${actualKey}` ===
interface CacheStats {
  hits: number;
  misses: number;
}
const cacheStats: CacheStats = { hits: 0, misses: 0 };
const restCache = new LRUCache<string, unknown>({
  max: 500,
  ttl: 5 * 60 * 1000,
});

function cacheGet<T>(key: string): T | undefined {
  const v = restCache.get(key);
  if (v === undefined) {
    cacheStats.misses++;
    return undefined;
  }
  cacheStats.hits++;
  return v as T;
}
function cacheSet(key: string, value: unknown): void {
  restCache.set(key, value);
}

// === SQLite (lazy-opened) ===
let _db: Database.Database | null = null;
function getDb(): Database.Database {
  if (!_db) {
    _db = new Database(SQLITE_PATH, { readonly: false });
    _db.pragma("journal_mode = WAL");
  }
  return _db;
}

const server = new McpServer({
  name: "observability",
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
  async ({ name, formal }) => {
    try {
      return {
        content: [{ type: "text", text: formal ? `Good day, ${name}.` : `Hello, ${name}!` }],
      };
    } catch (err) {
      // TODO (Task 4): replace this generic try/catch with a `withToolErrorHandling`
      // wrapper that logs structured error context (tool name, sub, args), sends a
      // sanitized message via notifications/message, and returns Zod-formatted
      // validation errors so the LLM can self-correct on its next call.
      logger.error("tool greet failed", { err });
      return { content: [{ type: "text", text: `greet failed: ${(err as Error).message}` }], isError: true };
    }
  },
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
  async ({ a, b }) => {
    try {
      return { content: [{ type: "text", text: String(a + b) }] };
    } catch (err) {
      logger.error("tool add_numbers failed", { err });
      return { content: [{ type: "text", text: `add_numbers failed: ${(err as Error).message}` }], isError: true };
    }
  },
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
      logger.error("tool fetch_url failed", { err, url });
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
  async ({ json, indent }) => {
    try {
      return {
        content: [{ type: "text", text: JSON.stringify(JSON.parse(json), null, indent ?? 2) }],
      };
    } catch (err) {
      logger.error("tool format_json failed", { err });
      return { content: [{ type: "text", text: `format_json failed: ${(err as Error).message}` }], isError: true };
    }
  },
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
    try {
      if (op === "divide" && b === 0) {
        return { content: [{ type: "text", text: "Cannot divide by zero." }], isError: true };
      }
      const result =
        op === "add" ? a + b : op === "subtract" ? a - b : op === "multiply" ? a * b : a / b;
      const sym = op === "add" ? "+" : op === "subtract" ? "-" : op === "multiply" ? "*" : "/";
      const structured = { result, expression: `${a} ${sym} ${b} = ${result}` };
      return {
        content: [{ type: "text", text: structured.expression }],
        structuredContent: structured,
      };
    } catch (err) {
      logger.error("tool calculate failed", { err });
      return { content: [{ type: "text", text: `calculate failed: ${(err as Error).message}` }], isError: true };
    }
  },
);

// === Lesson 16 work — completed and wired (your starting point for Lesson 18) ===

server.registerTool(
  "search_shipments",
  {
    title: "Search Shipments",
    description: "Search the caller's shipments. Filterable by status; cursor-paginated.",
    inputSchema: {
      query: z.string().describe("Substring match against shipment id and destination"),
      status: z.enum(["pending", "in_transit", "delivered", "delayed"]).optional(),
      limit: z.number().int().min(1).max(50).optional(),
      cursor: z.string().optional(),
    },
    outputSchema: {
      items: z.array(
        z.object({
          id: z.string(),
          query_match: z.string(),
          status: z.string(),
          owner_sub: z.string(),
        }),
      ),
      nextCursor: z.string().optional(),
    },
    annotations: { readOnlyHint: true },
  },
  async ({ query, status, limit, cursor }) => {
    try {
      const ctx = getCallerContext();
      const cacheKey = `${ctx.sub}:search:${query}:${status ?? ""}:${limit ?? 10}:${cursor ?? ""}`;

      let payload = cacheGet<{
        items: Array<{ id: string; query_match: string; status: string; owner_sub: string }>;
        nextCursor?: string;
      }>(cacheKey);

      if (!payload) {
        const url = new URL(`${MOCK_API_BASE}/shipments`);
        url.searchParams.set("query", query);
        if (status) url.searchParams.set("status", status);
        if (limit !== undefined) url.searchParams.set("limit", String(limit));
        if (cursor) url.searchParams.set("cursor", cursor);

        const res = await fetch(url, {
          headers: { Authorization: `Bearer ${ctx.bearerToken}` },
        });
        if (!res.ok) {
          return {
            content: [{ type: "text", text: `Upstream error ${res.status}: ${await res.text()}` }],
            isError: true,
          };
        }
        payload = (await res.json()) as typeof payload;
        cacheSet(cacheKey, payload);
      }

      // Defense in depth: drop anything not owned by the caller, even though
      // the upstream already filters.
      if (!payload) throw new Error("upstream returned empty payload");
      const items = payload.items.filter((s) => s.owner_sub === ctx.sub);
      const structured = { items, nextCursor: payload.nextCursor };
      return {
        content: [{ type: "text", text: JSON.stringify(structured, null, 2) }],
        structuredContent: structured,
      };
    } catch (err) {
      logger.error("tool search_shipments failed", { err });
      return {
        content: [{ type: "text", text: `search_shipments failed: ${(err as Error).message}` }],
        isError: true,
      };
    }
  },
);

server.registerTool(
  "get_shipment_history",
  {
    title: "Get Shipment History",
    description: "Read up to the last 50 history events for one of the caller's shipments.",
    inputSchema: {
      id: z.string().describe("Shipment id, e.g., SHIP-0001"),
    },
    outputSchema: {
      events: z.array(z.object({ ts: z.string(), event: z.string() })),
    },
    annotations: { readOnlyHint: true },
  },
  async ({ id }) => {
    try {
      const ctx = getCallerContext();
      const db = getDb();
      const stmt = db.prepare(
        "SELECT ts, event FROM shipments_history WHERE shipment_id = ? AND owner_sub = ? ORDER BY ts DESC LIMIT 50",
      );
      const rows = stmt.all(id, ctx.sub) as Array<{ ts: string; event: string }>;
      if (rows.length === 0) {
        return {
          content: [{ type: "text", text: `Shipment ${id} not found or not yours.` }],
          isError: true,
        };
      }
      const structured = { events: rows };
      return {
        content: [{ type: "text", text: JSON.stringify(structured, null, 2) }],
        structuredContent: structured,
      };
    } catch (err) {
      logger.error("tool get_shipment_history failed", { err, id });
      return {
        content: [{ type: "text", text: `get_shipment_history failed: ${(err as Error).message}` }],
        isError: true,
      };
    }
  },
);

server.registerTool(
  "record_delivery",
  {
    title: "Record Delivery",
    description: "Record a delivery for the caller's shipment. Requires scope shipments:write.",
    inputSchema: {
      id: z.string().describe("Shipment id"),
      signature: z.string().min(1).max(200).describe("Recipient signature"),
    },
    outputSchema: {
      id: z.string(),
      delivered_at: z.string(),
    },
    annotations: { destructiveHint: false, idempotentHint: true },
  },
  async ({ id, signature }) => {
    try {
      const ctx = getCallerContext();
      if (!ctx.scopes.includes("shipments:write")) {
        return {
          content: [
            {
              type: "text",
              text: "Missing scope: shipments:write. Re-authenticate with the broader scope.",
            },
          ],
          isError: true,
        };
      }
      const res = await fetch(`${MOCK_API_BASE}/shipments/${encodeURIComponent(id)}/deliveries`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${ctx.bearerToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ signature }),
      });
      if (!res.ok) {
        return {
          content: [{ type: "text", text: `Upstream error ${res.status}: ${await res.text()}` }],
          isError: true,
        };
      }
      const structured = (await res.json()) as { id: string; delivered_at: string };
      return {
        content: [{ type: "text", text: JSON.stringify(structured, null, 2) }],
        structuredContent: structured,
      };
    } catch (err) {
      logger.error("tool record_delivery failed", { err, id });
      return {
        content: [{ type: "text", text: `record_delivery failed: ${(err as Error).message}` }],
        isError: true,
      };
    }
  },
);

server.registerTool(
  "cache_stats",
  {
    title: "Cache Stats",
    description: "Return LRU cache hit-rate and the count of cache entries owned by the caller.",
    inputSchema: {},
    outputSchema: {
      hits: z.number(),
      misses: z.number(),
      hit_rate: z.number(),
      per_user_keys: z.number(),
    },
    annotations: { readOnlyHint: true },
  },
  async () => {
    try {
      const ctx = getCallerContext();
      const total = cacheStats.hits + cacheStats.misses;
      const hit_rate = total === 0 ? 0 : cacheStats.hits / total;
      let per_user_keys = 0;
      const prefix = `${ctx.sub}:`;
      for (const key of restCache.keys()) {
        if (typeof key === "string" && key.startsWith(prefix)) per_user_keys++;
      }
      const structured = {
        hits: cacheStats.hits,
        misses: cacheStats.misses,
        hit_rate,
        per_user_keys,
      };
      return {
        content: [{ type: "text", text: JSON.stringify(structured, null, 2) }],
        structuredContent: structured,
      };
    } catch (err) {
      logger.error("tool cache_stats failed", { err });
      return {
        content: [{ type: "text", text: `cache_stats failed: ${(err as Error).message}` }], isError: true,
      };
    }
  },
);

// === Express + Streamable HTTP transport (already wired) ======================

async function main() {
  // ===========================================================================
  // LESSON 18 — Six tasks. The starter compiles and runs out of the box; your
  // job is to harden it.
  //
  //   Task 1: Replace the `logger` stub at the top of this file with a real
  //           pino instance. Stream JSON lines to stderr. Honor LOG_LEVEL.
  //
  //   Task 2: Wire OpenTelemetry. See src/otel.ts for the NodeSDK scaffolding.
  //           Every tool call should produce a span; HTTP upstream calls
  //           should be child spans (auto-instrumentations-node will handle
  //           fetch/http for you once the SDK is started).
  //
  //   Task 3: Implement /healthz with REAL checks: SQLite reachable AND
  //           upstream REST API reachable (HEAD or GET on MOCK_API_BASE).
  //           Return 503 if any check fails; include the failing component
  //           in the response body. The current handler is a placeholder.
  //
  //   Task 4: Implement /livez. Process-alive only; no dependency checks.
  //           Returns 200 unless the server is shutting down (Task 6), in
  //           which case it should return 503.
  //
  //   Task 5: Wrap every tool with a `withToolErrorHandling(name, handler)`
  //           helper that:
  //             - wraps the call in `tracer.startActiveSpan(...)`
  //             - logs full error context (tool, sub, scopes, args) to stderr
  //             - returns Zod-formatted validation errors when applicable
  //             - sends a sanitized notifications/message to the client
  //           Replace each tool's inline try/catch.
  //
  //   Task 6: Graceful shutdown. On SIGTERM/SIGINT:
  //             1. stop accepting new connections
  //             2. flag a `shuttingDown = true` so /livez returns 503
  //             3. wait up to 10s for in-flight requests to finish
  //             4. close the SQLite handle and the OTel SDK
  //             5. process.exit(0)
  // ===========================================================================

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

  // .well-known/oauth-protected-resource — describes our auth requirements.
  app.get("/.well-known/oauth-protected-resource", (_req, res) => {
    res.json({
      resource: RESOURCE_URL,
      authorization_servers: [OAUTH_ISSUER],
      bearer_methods_supported: ["header"],
      scopes_supported: ["mcp:tools", "shipments:read", "shipments:write"],
    });
  });

  // TODO (Task 3): replace with real readiness checks (SQLite + upstream API).
  app.get("/healthz", (_req, res) => {
    res.status(200).json({ status: "ok", note: "placeholder — implement real checks in Task 3" });
  });

  // TODO (Task 4): replace with a process-alive check that returns 503 once
  // graceful shutdown begins.
  app.get("/livez", (_req, res) => {
    res.status(200).json({ status: "alive", note: "placeholder — implement Task 4" });
  });

  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: () => randomUUID(),
  });
  await server.connect(transport);

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

  const httpServer = app.listen(PORT, "127.0.0.1", () => {
    logger.info(`observability MCP server listening on http://127.0.0.1:${PORT}/mcp`);
  });

  // TODO (Task 6): register SIGTERM/SIGINT handlers to drain httpServer.close()
  // with a 10-second deadline before forcibly exiting. Close the SQLite handle
  // (_db?.close()) and the OTel SDK (await sdk.shutdown()) on the way out.
  void httpServer;
}

main().catch((err) => {
  logger.error("Fatal:", err);
  process.exit(1);
});
