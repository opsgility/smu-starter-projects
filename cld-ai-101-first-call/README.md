# CLD-AI-101 Lesson 3 — Your first Claude API call from Python

Starter for the first hands-on lab in the **Claude AI Engineer** path. You make your first calls to Claude from Python, read the response object, and inspect the token usage bill.

## Scenario

You are the new junior engineer at **Orion Analytics**, a mid-market data-analytics consultancy modernizing with AI. Your team lead has asked you to explore what Claude can do for the firm. Before you build anything, you need to feel out the shape of a real Claude call from Python — what goes in, what comes back, and what a request actually costs in tokens.

## Files

```
cld-ai-101-first-call/
  README.md                # this file
  .env.example             # ANTHROPIC_API_KEY (injected by lab proxy) + ANTHROPIC_MODEL default
  .gitignore               # .env, __pycache__, .venv
  requirements.txt         # Manifest only — packages already installed in the lab container.
  src/
    verify_env.py          # Smoke test — reads .env, one round-trip to Claude, exits 0/1.
    first_call.py          # Exercise 2 skeleton — TODO: your first client.messages.create call.
    inspect_response.py    # Exercise 3 skeleton — TODO: read content, stop_reason, usage.
```

## How to run

The lab container already ships the `anthropic` Python SDK preinstalled and the `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL` environment variables wired through the Claude API proxy at container start. You do NOT need to run `pip install`, bring your own Anthropic key, or create a `.env` file.

1. Open the integrated terminal in VS Code (**Terminal → New Terminal**). It opens at the workspace root — this starter's files (`src/`, `.env.example`, `requirements.txt`, etc.) are already there. You do NOT need to `cd` into a subfolder.
2. Smoke-test the environment: `python src/verify_env.py`. You should see `verify_env: OK — claude-sonnet-5 responded in Xs`.
3. Follow the exercises in the right-hand pane. They will point you at `src/first_call.py` and `src/inspect_response.py` in order.

> **Only if running locally against your own Anthropic account** (outside the SkillMeUp lab): `cp .env.example .env`, paste your key from `https://platform.claude.com/settings/keys`, and run as normal. Inside the lab container that step is unnecessary — the proxy already exported the env vars.

## Authentication

Every Anthropic API call authenticates with the `x-api-key` header — the `anthropic.Anthropic()` client reads that value from the `ANTHROPIC_API_KEY` environment variable. In production you would create the key at `platform.claude.com/settings/keys`. In this lab, the SkillMeUp Claude API proxy injects a shared platform key at container start so you can focus on the code, not on signup and key management.

## Notes

- Every model reference reads from `ANTHROPIC_MODEL` in the env — never hardcoded in source. This is deliberate. In L7's capstone you swap models by changing the env var, not by editing code.
- The current Claude model IDs you can use (as of 2026-09-27): `claude-haiku-4-5`, `claude-sonnet-5`, `claude-opus-5-5`, `claude-fable-5-1`. Old `claude-3-*` snapshot IDs are retired on the first-party API — do not use.
- The `requirements.txt` in this folder lists what the code needs so you can reproduce locally. Do not run `pip install -r requirements.txt` inside the lab container — the packages are already there.
