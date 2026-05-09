# Lesson 18 — Harden a Server with Logging and Error Recovery

Track 2 ends here. This starter is the **completed Lesson 16 API-wrapper server** — OAuth-protected Streamable HTTP, AsyncLocalStorage caller context, four shipments tools fully wired with per-user scoping, plus the LRU+TTL cache. **Deliberately bare on observability**: no logging, no health checks, no OpenTelemetry, no graceful shutdown. Your job is to wire it.

## What you will build

1. **Pino structured logging** — replace the `logger` stub at the top of `src/server.ts` with a real pino instance. JSON lines to stderr only. Honor `LOG_LEVEL`.
2. **OpenTelemetry tracing** — uncomment and import `src/otel.ts` at the very top of `src/server.ts` so the NodeSDK starts before any module is instrumented. Every tool call becomes a span; HTTP upstream calls auto-instrument as child spans.
3. **`/healthz` readiness check** — verify SQLite is reachable AND the upstream REST API is reachable. Return 503 if any check fails, with the failing component named in the body.
4. **`/livez` liveness check** — process-alive only. Returns 200 normally, 503 once shutdown begins.
5. **Tool error wrapping** — replace each tool's inline try/catch with a `withToolErrorHandling(name, handler)` helper that opens an OTel span, logs full error context (tool name, sub, scopes, args), returns Zod-formatted validation errors, and sends a sanitized `notifications/message` to the client.
6. **Graceful shutdown** — handle `SIGTERM`/`SIGINT`, drain in-flight requests with a 10-second timeout, close the SQLite handle, await `sdk.shutdown()`, then exit.

All six tasks are explained inline at the top of `main()` in `src/server.ts`.

## Running the three processes

You need three terminals.

### 1. Install (root, auth-server, mock-api)

```bash
npm install
(cd auth-server && npm install)
(cd mock-api && npm install)
```

### 2. Seed the SQLite DB

```bash
npm run build
npm run seed
```

### 3. Auth server (terminal 1)

```bash
npm run dev:auth
```

Listens on `http://127.0.0.1:4000`. Issue tokens with `curl -X POST 'http://127.0.0.1:4000/token?user=user-a'`.

### 4. Mock REST API (terminal 2)

```bash
npm run dev:mock
```

Listens on `http://127.0.0.1:5000`.

### 5. MCP resource server (terminal 3)

```bash
npm run dev:resource
```

Listens on `http://127.0.0.1:3000/mcp`.

### 6. Connect Claude Code

```bash
claude mcp add --transport http hardened-shipments http://127.0.0.1:3000/mcp
```

## Configuration

Copy `.env.example` to `.env`. New Lesson 18 vars:

| Var | Default | Purpose |
|---|---|---|
| `LOG_LEVEL` | `info` | Pino log level (Task 1) |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4318` | OTLP/HTTP collector (Task 2) |
| `OTEL_SERVICE_NAME` | `claude-mcp-lesson18-observability` | Span service name |

A local Jaeger / OTel collector exposing OTLP/HTTP on port 4318 is the easiest place to see spans.

## Verification

- Chaos test: kill the mock REST API while a `search_shipments` call is in flight. Claude Code should see a clean tool error (`isError: true`); the resource server's stderr should show a structured JSON line; `/healthz` should return 503 naming `mock-api`.
- Logs are valid JSON lines (one object per line).
- OTel spans for every tool call appear in your local Jaeger / collector.
- Sending `SIGTERM` to the resource server drains in-flight requests within 10s; `/livez` switches to 503 immediately; new connections are rejected.

## Notes

- Never `console.log` on an MCP server — `console.error` only. The `logger` stub at the top of `src/server.ts` only routes through console.error to keep that invariant intact until you replace it with pino.
- Import order matters for OTel — `import "./otel.js"` MUST be the first import in `src/server.ts` so the SDK starts before any instrumented module is required.
