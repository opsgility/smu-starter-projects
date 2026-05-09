# Lesson 6 Starter: Multi-Tool MCP Server

This starter contains the **completed code from Lesson 4** (`greet` and `add_numbers` tools) plus TODO scaffolds for three new tools you will implement in Lesson 6.

## What you will build

1. **`fetch_url`** — HTTPS-only HTTP fetcher with structured output (status, headers, body) and proper annotations.
2. **`format_json`** — pretty-print a JSON string using a Zod `.refine()` to validate input.
3. **`calculate`** — discriminated-union input for arithmetic ops with structured output.

Every tool must have BOTH `inputSchema` and `outputSchema`. Validation failures should return `{ isError: true, ... }`, not throw.

## How to start

```
npm install
npm run build
npm run inspect
```

Then add to Claude Code:

```
claude mcp add --scope local multi-tool node ./dist/server.js
```

## Critical rule (carried forward from Lesson 4)

Never use `console.log()` in stdio MCP servers — use `console.error()` for diagnostics.
