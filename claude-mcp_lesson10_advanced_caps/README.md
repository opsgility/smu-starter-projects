# Lesson 10 — Advanced Capabilities: Sampling, Roots, and Elicitation

This is the Lesson 10 starter for the **Building MCP Servers for Claude Code** course. It builds on the Lesson 8 server (resources + prompts) and adds TODO scaffolds for the three advanced MCP capabilities: **sampling**, **roots**, and **elicitation**.

## What's already built

- **Five tools** from Lessons 4 & 6 — `greet`, `add_numbers`, `fetch_url`, `format_json`, `calculate`.
- **Two resources** from Lesson 8:
  - Static `playbook://outage` reading `data/playbooks/outage.md`.
  - Templated `wiki://{slug}` reading `data/wiki/{slug}.md`.
- **One prompt** from Lesson 8 — `incident-triage` with `severity` and `service` arguments.

## What you'll add

Open `src/server.ts` and look for `// TODO (Task 1)` and `// TODO (Task 2)`. You'll implement two new tools:

1. **`summarize_file({ path })`** — uses **roots** to verify the path is authorized, reads the file, then uses **sampling** (`server.server.createMessage(...)`) to ask the host model for a 3-bullet summary. Returns structured output `{ summary: string[], path: string }`.

2. **`generate_commit_message({ diff })`** — uses **elicitation** (`server.server.elicitInput(...)`) to ask the user for `{ scope, breaking_change }`, then uses sampling to produce a Conventional Commits message. Must handle the user clicking **Cancel** cleanly.

The TODO blocks include the full API surface (request shapes, response shapes, spec links) so you can fill in the bodies without leaving the file.

## How to start

```bash
npm install
npm run build
npm run inspect
```

`npm run inspect` launches MCP Inspector against your built server. Connect, then exercise each tool from the Tools panel.

## How to test root enforcement (Task 3)

After implementing `summarize_file`, in MCP Inspector:

1. In the Inspector UI, configure a root pointing at this project (e.g. `file:///workspaces/claude-mcp_lesson10_advanced_caps`).
2. Call `summarize_file` with a path **inside** the root (e.g. `./README.md`) — should succeed.
3. Call `summarize_file` with `path: "/tmp/secrets.txt"` — should return `{ isError: true, content: [...] }` with a clear "outside authorized roots" message. **It must NOT read the file.**

## How to test elicitation cancellation (Task 4)

After implementing `generate_commit_message`, register the server in Claude Code 2.1.76+ (`claude mcp add --scope local advanced-caps node ./dist/server.js`), then ask Claude to call `generate_commit_message` with any diff.

1. The elicitation dialog should appear in Claude Code.
2. Click **Cancel** in the dialog.
3. The tool should return a friendly text message ("Commit message generation was canceled by the user.") with `isError: false` — **not** a JSON-RPC error and **not** a thrown exception.

## File layout

```
.
├── data/
│   ├── playbooks/outage.md
│   └── wiki/{intro,onboarding,incident-response}.md
├── src/server.ts          # all the code
├── package.json
├── tsconfig.json
└── README.md
```

## Conventions

- TypeScript ES2022 / ESM.
- `console.error` only — never `console.log` (it would corrupt the stdio JSON-RPC stream).
- Every tool has both `inputSchema` and `outputSchema` where it returns structured data.
