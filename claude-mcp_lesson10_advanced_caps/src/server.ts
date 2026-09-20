#!/usr/bin/env node
import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = resolve(__dirname, "..", "data");

// === Capability Declarations (educational comment) ===
//
// The McpServer instance below auto-negotiates capabilities with the client
// during the JSON-RPC `initialize` exchange. The SDK declares server
// capabilities for tools, resources, and prompts based on what you
// register. For the Lesson 10 features (sampling, roots, elicitation),
// the *client* must advertise support — Claude Code 2.1.76+ does so.
//
// In a fully-typed initialize handshake, the client capabilities object
// looks like:
//
//   {
//     "capabilities": {
//       "roots":       { "listChanged": true },
//       "sampling":    {},
//       "elicitation": {}
//     }
//   }
//
// On the server side you don't have to do anything to OPT IN — calling
// `server.server.listRoots()`, `server.server.createMessage(...)`, or
// `server.server.elicitInput(...)` will simply throw at runtime if the
// connected client did not declare the matching capability. Plan for that:
// always check for a connected client that supports the feature, or wrap
// the call in try/catch and return `isError: true` with a friendly hint
// that the user's MCP client doesn't support sampling/roots/elicitation.
//
// Spec references:
//   - Roots:       https://modelcontextprotocol.io/specification/2025-11-25/client/roots
//   - Sampling:    https://modelcontextprotocol.io/specification/2025-11-25/client/sampling
//   - Elicitation: https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation
// =====================================================

const server = new McpServer({
  name: "advanced-caps",
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

// === Lesson 8 completed work — resources and prompts ===

// Static resource: playbook://outage
server.registerResource(
  "outage-playbook",
  "playbook://outage",
  {
    title: "Outage Response Playbook",
    description: "The canonical Northwind on-call outage runbook.",
    mimeType: "text/markdown",
  },
  async (uri) => {
    const text = await readFile(resolve(DATA_DIR, "playbooks", "outage.md"), "utf8");
    return {
      contents: [
        {
          uri: uri.href,
          mimeType: "text/markdown",
          text,
        },
      ],
    };
  },
);

// Templated resource: wiki://{slug}
const wikiTemplate = new ResourceTemplate("wiki://{slug}", { list: undefined });
server.registerResource(
  "wiki",
  wikiTemplate,
  {
    title: "Northwind Wiki",
    description: "Internal Northwind engineering wiki pages, addressed by slug.",
    mimeType: "text/markdown",
  },
  async (uri, { slug }) => {
    const slugStr = Array.isArray(slug) ? slug[0] : slug;
    const text = await readFile(resolve(DATA_DIR, "wiki", `${slugStr}.md`), "utf8");
    return {
      contents: [
        {
          uri: uri.href,
          mimeType: "text/markdown",
          text,
        },
      ],
    };
  },
);

// Prompt: incident-triage
server.registerPrompt(
  "incident-triage",
  {
    title: "Incident Triage",
    description: "Walk an on-call engineer through the first ten minutes of an incident for a given severity and service.",
    argsSchema: {
      severity: z.enum(["low", "med", "high", "critical"]).describe("Incident severity"),
      service: z.string().describe("Affected service name"),
    },
  },
  ({ severity, service }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text:
            `You are an experienced incident commander at Northwind Logistics. ` +
            `Triage rules: acknowledge within 5 minutes, declare a commander, mitigate before root-causing, ` +
            `communicate every 15 minutes, and schedule a blameless postmortem within 48 hours.\n\n` +
            `A ${severity}-severity incident has just been declared on the "${service}" service. ` +
            `Walk me through the first ten minutes step by step, in order, calling out who pages whom and which channels open.`,
        },
      },
    ],
  }),
);

// === Lesson 10 work goes here — Sampling, Roots, and Elicitation ===

// TODO (Task 1): Implement `summarize_file({ path: string })`.
//
// REQUIRED FLOW:
//   1. Call `server.server.listRoots()` to ask the client which directories
//      it has authorized this server to read. The response is shaped like:
//        { roots: [{ uri: 'file:///workspaces/myrepo', name?: '...' }, ...] }
//      See https://modelcontextprotocol.io/specification/2025-11-25/client/roots
//
//   2. Validate `path` is INSIDE one of those roots. Strategy:
//        - Resolve `path` to an absolute path with `path.resolve(path)`.
//        - For each root, convert its `uri` to a filesystem path with
//          `fileURLToPath(root.uri)`, then check that the resolved path
//          starts with `<rootPath>` + path.sep (or equals it).
//        - If no root matches, return `{ isError: true, content: [{ type: 'text', text: '...refused...' }] }`.
//        - "What Could Go Wrong?" — symlinks. If you want to be airtight,
//          call `fs.realpath(path)` BEFORE comparing.
//
//   3. Read the file with `await readFile(path, 'utf8')`.
//
//   4. Ask the host model for a 3-bullet summary via sampling:
//        const result = await server.server.createMessage({
//          messages: [
//            { role: 'user', content: { type: 'text',
//                text: `Summarize the following file in exactly 3 short bullet points. Return only the bullets.\n\n${contents}` } }
//          ],
//          maxTokens: 400,
//          modelPreferences: {
//            hints: [{ name: 'claude-3-5-sonnet' }],
//            costPriority: 0.3,
//            speedPriority: 0.5,
//            intelligencePriority: 0.7,
//          },
//          systemPrompt: 'You produce concise technical summaries.',
//        });
//      The response shape: { role: 'assistant', content: { type: 'text', text: '...' }, model: '...', stopReason: '...' }.
//      See https://modelcontextprotocol.io/specification/2025-11-25/client/sampling
//
//   5. Parse the bullets out of the assistant text into a string[]
//      (split on newlines, strip leading "-", "*", or "•").
//
//   6. Return BOTH a plain-text rendering and structured output:
//        return {
//          content: [{ type: 'text', text: bullets.map(b => `• ${b}`).join('\n') }],
//          structuredContent: { summary: bullets, path: resolvedPath },
//        };
//
// SCHEMAS:
//   inputSchema:  { path: z.string().describe('Absolute or workspace-relative file path to summarize') }
//   outputSchema: { summary: z.array(z.string()), path: z.string() }
//
// server.registerTool(
//   "summarize_file",
//   {
//     title: "Summarize File",
//     description: "Summarize a file's contents in 3 bullet points using the host model. Path must be inside a client-declared root.",
//     inputSchema:  { path: z.string() },
//     outputSchema: { summary: z.array(z.string()), path: z.string() },
//     annotations:  { readOnlyHint: true },
//   },
//   async ({ path }) => {
//     // 1) listRoots, 2) validate, 3) readFile, 4) createMessage, 5) parse bullets, 6) return.
//   },
// );

// TODO (Task 2): Implement `generate_commit_message({ diff: string })`.
//
// REQUIRED FLOW:
//   1. Use elicitation to ask the user for `{ scope: string, breaking_change: boolean }`:
//        const elicit = await server.server.elicitInput({
//          message: 'Help me craft a Conventional Commits message for this diff.',
//          requestedSchema: {
//            type: 'object',
//            properties: {
//              scope: {
//                type: 'string',
//                description: 'Component / scope (e.g. "api", "auth", "ui"). Leave blank for none.',
//              },
//              breaking_change: {
//                type: 'boolean',
//                description: 'Does this change break the public API?',
//              },
//            },
//            required: ['scope', 'breaking_change'],
//          },
//        });
//      See https://modelcontextprotocol.io/specification/2025-11-25/client/elicitation
//
//   2. Handle the THREE response actions cleanly:
//        - elicit.action === 'accept'   → use elicit.content as the values
//        - elicit.action === 'cancel'   → return a friendly cancellation:
//             return {
//               content: [{ type: 'text', text: 'Commit message generation was canceled by the user.' }],
//               isError: false,
//             };
//        - elicit.action === 'decline'  → similar to cancel, but the user
//             refused to provide info. Same friendly return is fine.
//
//   3. With the accepted values, call sampling:
//        const result = await server.server.createMessage({
//          messages: [{ role: 'user', content: { type: 'text', text:
//            `Write a single-line Conventional Commits message for the following diff. ` +
//            `Scope: "${scope || 'none'}". Breaking change: ${breaking_change}. ` +
//            `Format: <type>(<scope>): <description>  — add a trailing "!" before the colon if breaking. ` +
//            `Diff:\n\n${diff}` } }],
//          maxTokens: 100,
//          modelPreferences: { intelligencePriority: 0.6, speedPriority: 0.7 },
//        });
//
//   4. Return the generated commit message as content + structured output:
//        return {
//          content: [{ type: 'text', text: message }],
//          structuredContent: { message, scope, breakingChange: breaking_change },
//        };
//
// SCHEMAS:
//   inputSchema:  { diff: z.string().describe('The git diff (output of `git diff --staged`) to summarize as a commit message') }
//   outputSchema: { message: z.string(), scope: z.string(), breakingChange: z.boolean() }
//
// server.registerTool(
//   "generate_commit_message",
//   {
//     title: "Generate Commit Message",
//     description: "Ask the user for scope + breaking-change flag (via elicitation), then sample the host model to produce a Conventional Commits message.",
//     inputSchema:  { diff: z.string() },
//     outputSchema: { message: z.string(), scope: z.string(), breakingChange: z.boolean() },
//   },
//   async ({ diff }) => {
//     // 1) elicitInput, 2) handle action, 3) createMessage, 4) return.
//   },
// );

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("advanced-caps MCP server connected on stdio");
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
