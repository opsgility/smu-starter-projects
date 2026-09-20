# Lesson 20 Capstone — Build, Document, and Publish Your Own MCP Server

This is the capstone project for *Building MCP Servers for Claude Code*. You will design and ship a production-quality MCP server end to end: source, tests, lint, CI, MCPB bundle, and registry-ready `server.json`.

This scaffold is **standalone** — it is not a fork of either track chain. Pick one of three tracks below.

## 1. Pick Your Track

| Track | Domain | Required Capabilities |
|-------|--------|-----------------------|
| **A — DevOps** | Wrap a Kubernetes cluster (read-only) | Tools (list pods, describe deployment, get logs), Resources (manifest YAMLs), Roots enforcement, structured output |
| **B — Knowledge** | Wrap a Notion/Confluence-style wiki API | Tools (search, read), Resource templates with URI scheme, Prompts (template for writing a doc), Elicitation for confirmation |
| **C — Data** | Read-only Postgres analytics server | Tools (run SELECT with row caps), Resources (schema introspection), OAuth 2.1, Sampling for query summarization |

Track-specific code lives under `src/track-a/`, `src/track-b/`, or `src/track-c/`. **Delete the two folders you are not using before you commit.**

## 2. Required Deliverables (all 10)

1. TypeScript source with full Zod **`inputSchema` AND `outputSchema`** on every tool.
2. At least one tool, one resource (template or static), and one prompt.
3. `console.error`-only logging on stdio; `notifications/message` for user-visible logs.
4. Either Streamable HTTP + OAuth 2.1 (Tracks B and C) **OR** stdio + Roots enforcement (Track A).
5. MCP Inspector trace showing every primitive working.
6. `README.md` with installation instructions for Claude Code (`claude mcp add ...`).
7. `manifest.json` for an MCPB bundle build.
8. `server.json` ready for registry submission (does not have to be actually submitted).
9. At least 3 unit tests for tool handlers (use `vitest`).
10. A short demo recording (or screenshot sequence) of the server running inside Claude Code.

## 3. Validation Criteria (the 7 the left agent checks)

- `src/server.ts` exists and `npm run build` succeeds without errors.
- `npm test` passes with at least 3 passing tests.
- Every tool has both `inputSchema` AND `outputSchema`.
- No `console.log` calls anywhere (`grep -rn "console.log" src/` returns zero results).
- `manifest.json` validates against the MCPB schema.
- `README.md` includes the exact `claude mcp add` command and a "Tools" section listing every tool.
- Server connects successfully in Claude Code AND in MCP Inspector.

## 4. Run It

```bash
npm install
npm run build
npm test
npm run inspect          # opens MCP Inspector against your built server
npm run lint
npm run format
npm run pack:mcpb        # produces a .mcpb bundle for distribution
```

## 5. Register With Claude Code

For a stdio server (Track A):

```bash
claude mcp add --scope local capstone node ./dist/server.js
```

For a Streamable HTTP server (Tracks B and C):

```bash
claude mcp add --transport http capstone http://127.0.0.1:3000/mcp
```

Then in Claude Code, type `@` to discover resources and `/` to discover prompts. Use `claude mcp list` to confirm the server is connected.

## 6. File Layout

```
.
|-- src/
|   |-- server.ts          # entry point — register tools/resources/prompts here
|   |-- lib/
|   |   `-- auth.ts        # OAuth helper stub (Tracks B & C)
|   |-- track-a/           # DevOps track (delete if not chosen)
|   |-- track-b/           # Knowledge track (delete if not chosen)
|   `-- track-c/           # Data track (delete if not chosen)
|-- tests/
|   |-- server.test.ts
|   `-- tools.test.ts
|-- manifest.json          # MCPB bundle manifest
|-- server.json            # Official MCP Registry manifest
|-- .github/workflows/ci.yml
|-- package.json
|-- tsconfig.json
|-- vitest.config.ts
|-- .eslintrc.json
`-- .prettierrc.json
```

## 7. Tools

Replace this section with one bullet per tool you implement, listing name, purpose, and input fields. The validator checks for the literal heading `## Tools` and at least one tool listed.

- *(your tool here)*

## 8. Where To Look For Help

- Lesson 6 starter — multi-tool stdio patterns (`fetch_url`, `format_json`, `calculate`).
- Lesson 8 starter — resources + prompts.
- Lesson 10 starter — sampling, roots, elicitation.
- Lesson 12 starter — Streamable HTTP transport.
- Lesson 14 starter — OAuth 2.1 + PKCE + JWT validation.
- Lesson 16 starter — API-wrapper patterns and per-user data scoping.
- Lesson 18 starter — `pino` logging, OpenTelemetry, health checks, graceful shutdown.

The left agent will help you, but only after you've identified your track and made a first attempt.
