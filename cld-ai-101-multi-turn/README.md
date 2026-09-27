# CLD-AI-101 Lesson 5 — Building a multi-turn conversation with Claude

Starter for the second hands-on lab in the **Claude AI Engineer** path. You build a small multi-turn REPL against Claude with a top-level system prompt, and convert it to a streaming response.

## Scenario

You are the junior engineer at **Orion Analytics** who just finished the first Claude API call in L3. Your team lead wants to see whether Claude can act as a small support-triage helper for the analytics team — a REPL an on-call engineer would run at a terminal. That means multi-turn conversation state and, eventually, a streaming response so the reply prints token-by-token instead of all-at-once at the end.

## Files

```
cld-ai-101-multi-turn/
  README.md                # this file
  .env.example             # ANTHROPIC_API_KEY (injected by lab proxy) + ANTHROPIC_MODEL default
  .gitignore               # .env, __pycache__, .venv
  requirements.txt         # Manifest only — packages already installed in the lab container.
  src/
    verify_env.py          # Smoke test — reads .env, one round-trip to Claude, exits 0/1.
    repl.py                # Exercise 2 skeleton — TODO: build the multi-turn conversation loop.
    streaming.py           # Exercise 4 skeleton — TODO: convert the loop to a streaming response.
```

## How to run

Same container contract as L3 — `anthropic` SDK preinstalled, `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL` exported into the container's shell by the proxy at container start. No `pip install`, no signup, no `.env` file to create.

1. Open a terminal (**Terminal → New Terminal**). It opens at the workspace root, where this starter's files already live. No `cd` into a subfolder needed.
2. Smoke-test: `python src/verify_env.py` → expect `verify_env: OK`.
3. Follow the exercises. `repl.py` first, then `streaming.py`.

> **Only if running locally against your own Anthropic account**: `cp .env.example .env`, paste your key, and run as normal. Inside the lab the env is already ready.

## Authentication

Same as L3 — `anthropic.Anthropic()` reads `ANTHROPIC_API_KEY` from env, injected by the lab proxy. No key management inside this lab.

## Notes

- **System prompt goes in the top-level `system=` parameter**, not as a `{"role": "system"}` message. This is a common confusion for people coming from other LLM APIs; the Messages API is explicit about it.
- **Conversation state = list of `{"role": ..., "content": ...}` dicts.** Claude has no persistent memory — you re-send the whole history on every turn. The `messages` array IS your memory.
- **Streaming**: `client.messages.stream(...)` returns a context manager. Iterate `stream.text_stream` for token-by-token text; call `stream.get_final_message()` after the stream closes if you want the full `Message` object with usage.
- **Stop reasons you'll see:** `end_turn` (normal finish), `max_tokens` (hit the cap you set), `stop_sequence` (matched a stop_sequences pattern), `model_context_window_exceeded` (input + output would overflow context — you'll hit this deliberately in Exercise 3).
