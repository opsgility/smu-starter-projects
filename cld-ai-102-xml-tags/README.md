# CLD-AI-102 Lesson 2 — Structure a triage prompt with XML tags

Starter for the first hands-on lab in the **Prompt Engineering with Claude** course. You take Orion Analytics' brittle L5-era triage bot, rewrite it with XML tags (input separation + output shaping), measure the parse-failure-rate drop on 10 real-shape tickets, and see the *security* payoff of input tags with your own eyes.

## Scenario

You're the junior engineer at **Orion Analytics** — same mid-market data-analytics consultancy from CLD-AI-101. Your L5-era triage bot works ~90% of the time on categorization but has a nasty ~40% parse-failure rate: Claude replies in varied phrasings and your Python parser (`if "Category:" in reply`) misses. Your team lead asked you to rewrite the prompt with XML tags after the L1 teaching lesson. This lab is that rewrite, plus quantitative before/after evidence.

## Files

```
cld-ai-102-xml-tags/
  README.md                        # this file
  .env.example                     # ANTHROPIC_API_KEY (injected by lab proxy) + ANTHROPIC_MODEL default
  .gitignore                       # .env, __pycache__, .venv
  requirements.txt                 # Manifest only — packages already installed in the lab container.
  data/
    tickets.json                   # 10 real-shape Orion tickets (mixed categories + edge cases)
  src/
    verify_env.py                  # Smoke test — reads .env, one round-trip to Claude, exits 0/1.
    triage_v1_unstructured.py      # Reference — Orion's L5-era prompt, no XML tags (COMPLETE, do not edit).
    triage_v2_xml.py               # Exercise 2 skeleton — TODO: add <ticket> input + <category>/<next_step> output tags.
    measure_parse_rate.py          # Exercise 3 script — runs both versions across data/tickets.json, prints a comparison table.
    instruction_confusion_demo.py  # Exercise 4 script — one crafted ticket that breaks v1 and survives v2.
```

## How to run

The lab container already ships the `anthropic` Python SDK preinstalled and the `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL` environment variables wired through the Claude API proxy at container start. You do NOT need to run `pip install`, bring your own Anthropic key, or create a `.env` file.

1. Open the integrated terminal in VS Code (**Terminal → New Terminal**). It opens at the workspace root — this starter's files (`src/`, `data/`, `.env.example`, etc.) are already there. You do NOT need to `cd` into a subfolder.
2. Smoke-test the environment: `python src/verify_env.py`. You should see `verify_env: OK — claude-sonnet-5 responded in Xs`.
3. Follow the exercises in the right-hand pane. They will point you at each `src/*.py` file in order.

> **Only if running locally against your own Anthropic account** (outside the SkillMeUp lab): `cp .env.example .env`, paste your key from `https://platform.claude.com/settings/keys`, and run as normal. Inside the lab container that step is unnecessary — the proxy already exported the env vars.

## Authentication

Every Anthropic API call authenticates with the `x-api-key` header — the `anthropic.Anthropic()` client reads that value from the `ANTHROPIC_API_KEY` environment variable. In production you would create the key at `platform.claude.com/settings/keys`. In this lab, the SkillMeUp Claude API proxy injects a shared platform key at container start so you can focus on the code, not on signup and key management.

## What you'll practice

- **Input separation** — wrap unstructured content (`<ticket>...</ticket>`) so Claude reads it as data-to-analyze, not instructions-to-follow.
- **Output shaping** — ask Claude to reply inside specific tags (`<category>...</category>`, `<next_step>...</next_step>`) so downstream parsing collapses to one line of `xml.etree.ElementTree`.
- **Safe text extraction** — `next((b.text for b in resp.content if b.type == "text"), "")` — the same CLD-AI-101 pattern that survives adaptive-thinking model swaps.
- **Instruction-confusion defense** — the specific security case where a ticket containing "Please tell the customer to..." would leak-instruction-inject a tag-less prompt and gets neutralized once wrapped in `<ticket>` tags.

## Notes

- Every model reference reads from `ANTHROPIC_MODEL` in the env — never hardcoded in source.
- Current Claude model IDs you can use (as of 2026-09-27): `claude-haiku-4-5`, `claude-sonnet-5`, `claude-opus-5-5`, `claude-fable-5-1`. Old `claude-3-*` snapshot IDs are retired on the first-party API — do not use.
- Parsing uses `xml.etree.ElementTree` (Python stdlib). No extra dependency; wrap Claude's reply in a synthetic `<r>...</r>` root before `.find(...)` so multiple sibling output tags parse cleanly.
