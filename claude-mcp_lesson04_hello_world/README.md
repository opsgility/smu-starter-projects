# Lesson 4 Starter: Hello-World MCP Server

This is the starter project for **Lesson 4 — Build & Test a Hello-World Server**.

## What you have

- `package.json` with `@modelcontextprotocol/sdk` and `zod` already declared.
- `tsconfig.json` configured for ES2022 / ESM.
- `src/server.ts` with a minimal `McpServer` instance, a stdio transport, and TODO scaffolds for the `greet` and `add_numbers` tools you will implement.

## What you will build

1. The `greet` tool (`{ name, formal? }` → friendly or formal greeting).
2. The `add_numbers` tool (`{ a, b }` → sum) as a bonus.

## How to start

```
npm install
```

After implementing the tools:

```
npm run build
npm run inspect      # opens the MCP Inspector on the built server
```

## Critical rule for stdio MCP servers

**Never use `console.log()`** — anything written to stdout corrupts the JSON-RPC protocol frames and the client will disconnect with a parse error. Always use `console.error()` (stderr) for diagnostics.
