# RetireScope — Lesson 15 Starter

The AI Portfolio Assistant: Anthropic Claude with tool use answering portfolio questions by calling your existing functions. SSE-streamed responses with visible tool calls in the chat UI.

## Getting Started

```bash
npm install
npm run dev
```

In another terminal:

```bash
web-tunnel
```

Open the public URL, navigate to **AI Assistant**, and ask:


> **Don't use the `/proxy/3000/` URL** that VS Code surfaces — Next.js's Turbopack dev server emits absolute `/_next/static/...` URLs that don't resolve through code-server's path-prefixed proxy. Always view the app through the `web-tunnel` ngrok URL instead.


- "What's my portfolio worth?"
- "Show me my asset allocation."
- "If I retire at 65 with $1.5M and withdraw $60k/year for 30 years, will I be okay?"
- "I need $40,000 next year — what's the most tax-efficient way to take it?"

## What's New (Module 7 → Module 8)

- `lib/ai/anthropic.ts` — SDK client + model constants
- `lib/ai/system-prompt.ts` — assistant persona
- `lib/ai/tools.ts` — 5 tool schemas: `get_portfolio_summary`, `list_accounts`, `get_allocation`, `run_projection`, `plan_withdrawal`
- `lib/ai/tool-handlers.ts` — dispatchers that wrap your existing finance functions
- `app/api/assistant/route.ts` — SSE streaming endpoint with the agentic loop
- `components/assistant/chat-panel.tsx` — Client Component with tool-call visualization
- `app/(dashboard)/assistant/page.tsx` — full implementation
- New deps: `@anthropic-ai/sdk`, `react-markdown`

## Configuration

In the lab container, `ANTHROPIC_BASE_URL` and `ANTHROPIC_API_KEY` are auto-injected. Outside the lab, set them in `.env.local`.

## What You'll Build in Lesson 15

The complete AI assistant with multi-turn tool use, error handling, and the final polish.
