# Lesson 12 — Convert Your Server to Streamable HTTP

Track 2 starts here. This starter is a clean fork of the completed Lesson 6 multi-tool server. All five tools are already implemented:

- `greet` — formal/informal greeting.
- `add_numbers` — sum of two numbers.
- `fetch_url` — HTTPS-only fetch with structured `{ status, headers, body }` output.
- `format_json` — pretty-print a JSON string with `.refine()` validation.
- `calculate` — `add | subtract | multiply | divide` with structured output.

Your job in this lesson is to swap the transport from `StdioServerTransport` to `StreamableHTTPServerTransport`.

## Setup

```bash
npm install
npm run build
npm start
```

The starter still ships with stdio transport so it compiles out of the box. You will replace this in Tasks 1 and 2.

## Tasks

1. Add Express + `StreamableHTTPServerTransport`; replace `StdioServerTransport`.
2. Implement session management with `sessionIdGenerator`; add an `Origin` allowlist middleware; bind to `127.0.0.1`.
3. Build and run; test with MCP Inspector in HTTP transport mode.
4. Register in Claude Code:

   ```bash
   claude mcp add --transport http local-http http://127.0.0.1:3000/mcp
   ```

5. Test concurrent sessions: open two Claude Code instances pointing at the same server and confirm `Mcp-Session-Id` round-trips correctly.

## Verification

- Server accepts concurrent sessions.
- `Mcp-Session-Id` round-trips correctly between client and server.
- A request with a non-allowlisted `Origin` header is rejected with HTTP 403.
- The server binds to `127.0.0.1` only — never `0.0.0.0`.

## Configuration

Top of `src/server.ts`:

```ts
const PORT = 3000;
const ALLOWED_ORIGINS = new Set<string>(["http://localhost", "http://127.0.0.1"]);
```

## Notes

- Never `console.log` on an MCP server — use `console.error` only.
- Bind to `127.0.0.1`, not `0.0.0.0`, to defend against DNS-rebinding attacks during local development.
