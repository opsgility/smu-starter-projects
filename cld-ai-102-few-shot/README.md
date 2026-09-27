# CLD-AI-102 Lesson 4 — Building a few-shot ticket classifier

Starter for the second hands-on lab in the **Prompt Engineering with Claude** course. You take your L2 v2 XML-tagged classifier, layer 3 hand-picked few-shot examples on top, and measure the accuracy delta across 20 tickets (10 typical + 10 edge cases). Ex 3 builds a deliberately-bad "all-Billing examples" ablation so you can see with your own eyes that BAD examples hurt accuracy below zero-shot — a critical intuition for choosing examples well in production.

## Scenario

You're the junior engineer at **Orion Analytics** (same setup as CLD-AI-101 and L2). Your v2 XML-tagged classifier from L2 hits 99% parse rate but only ~85% categorization accuracy. The team lead asked you to try few-shot prompting per L3. This lab is the rewrite plus quantitative before/after evidence across 20 tickets — with a specific ablation showing what happens when you pick BAD examples.

## Files

```
cld-ai-102-few-shot/
  README.md                  # this file
  .env.example               # ANTHROPIC_API_KEY (injected by lab proxy) + ANTHROPIC_MODEL default
  .gitignore                 # .env, __pycache__, .venv
  requirements.txt           # Manifest only — packages already installed in the lab container.
  data/
    tickets.json             # 20 tickets: 10 typical (like L2) + 10 edge cases (cancellations-with-features, tech-with-billing-hint, snippy one-liners)
  src/
    verify_env.py            # Smoke test — reads .env, one round-trip to Claude, exits 0/1.
    triage_zero_shot.py      # L2's v2 (COMPLETE, do not edit) — the baseline you're improving on.
    triage_few_shot.py       # Exercise 2 skeleton — TODO: add 3 well-chosen edge-case few-shot examples.
    triage_few_shot_bad.py   # Exercise 3 skeleton — TODO: add 3 all-Billing examples (deliberately bad).
    measure_accuracy.py      # Exercise 4 script — runs all 3 versions across data/tickets.json, prints accuracy comparison.
```

## How to run

The lab container already ships the `anthropic` Python SDK preinstalled and the `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL` environment variables wired through the Claude API proxy at container start. You do NOT need to run `pip install`, bring your own Anthropic key, or create a `.env` file.

1. Open the integrated terminal in VS Code (**Terminal → New Terminal**). It opens at the workspace root.
2. Smoke-test the environment: `python src/verify_env.py`.
3. Follow the exercises in the right-hand pane. They point at each `src/*.py` in order.

> **Only if running locally against your own Anthropic account** (outside the SkillMeUp lab): `cp .env.example .env`, paste your key from `https://platform.claude.com/settings/keys`, and run as normal.

## What you'll practice

- **Few-shot prompting** — layering 3 worked `<example><input>...</input><output>...</output></example>` blocks on top of the L2 XML-tagged prompt.
- **Choosing edge-case examples** — pick tickets from the confusion set (cancellations-with-features, technical-with-billing-hints) rather than typical ones.
- **The ablation intuition** — see that BAD examples (all-Billing) drop accuracy BELOW zero-shot, not just fail to help. Critical production lesson: example selection matters more than example COUNT.
- **Same parse-safe output** — the `<category>` + `<next_step>` output tags and one-line `xml.etree` parser from L2 are unchanged.

## Notes

- Every model reference reads from `ANTHROPIC_MODEL` in the env — never hardcoded in source.
- Current Claude model IDs you can use (as of 2026-09-27): `claude-haiku-4-5`, `claude-sonnet-5`, `claude-opus-5-5`, `claude-fable-5-1`. Old `claude-3-*` snapshot IDs are retired on the first-party API.
- All 3 triage_*.py files share the same shape so `measure_accuracy.py` can import and compare them head-to-head.
