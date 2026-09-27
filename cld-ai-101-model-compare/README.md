# CLD-AI-101 Lesson 7 — Same prompt, three models: measuring cost, latency, and quality

Starter for the **capstone** hands-on lab in CLD-AI-101. You benchmark the same three prompts across Haiku 4.5, Sonnet 5, and Opus 5.5 — log token counts, wall-clock latency, computed cost per model, and a small human- or LLM-judged quality score — and produce a written recommendation for Orion Analytics' team lead on which model to standardize on.

## Scenario

Orion Analytics' team lead needs a recommendation before the team starts building a client-facing chatbot: which Claude model should the chatbot standardize on? You are the junior engineer running the benchmark. Bring back numbers, not vibes.

## Files

```
cld-ai-101-model-compare/
  README.md                # this file
  .env.example             # ANTHROPIC_API_KEY (injected by lab proxy)
  .gitignore               # .env, __pycache__, .venv, results/
  requirements.txt         # Manifest only — packages already installed in the lab container.
  src/
    verify_env.py          # Smoke test — one round-trip to Claude, exits 0/1.
    benchmark.py           # Exercise 1 skeleton — TODO: run the 3-prompt x 3-model matrix.
    pricing.py             # Per-model pricing dict — used in Exercise 2 for cost math.
  data/
    prompts.txt            # The three test prompts + notes on what each measures.
```

## How to run

Same container contract as L3 / L5 — `anthropic` preinstalled, `ANTHROPIC_API_KEY` + `ANTHROPIC_BASE_URL` already exported into the container's shell by the proxy at container start.

1. Open a terminal — it opens at the workspace root, where this starter's files already live. No `cd` into a subfolder needed; no `.env` file to create.
2. `python src/verify_env.py` — expect `verify_env: OK`.
3. Follow the exercises in the right-hand pane.

> **Only if running locally against your own Anthropic account**: `cp .env.example .env`, paste your key, and run as normal. Inside the lab the env is already ready.

## Authentication

Same as L3 / L5 — no key management inside this lab.

## Notes

- Every model reference in `benchmark.py` reads from a list — Haiku 4.5, Sonnet 5, Opus 5.5. Fable 5.1 is deliberately excluded from this benchmark; at $10 / $50 per MTok it's too expensive to spray for a foundation-tier exercise, and its capability profile is discussed in the L6 teaching lesson.
- **Pricing** lives in `src/pricing.py` as a `{model_id: (input_price_per_MTok, output_price_per_MTok)}` dict. The values are current as of the lab authoring date — if you're running this locally months later, check the current numbers at https://platform.claude.com/docs/en/docs/about-claude/pricing before drawing conclusions.
- **The quality-rating step** uses `claude-sonnet-5` as an LLM-judge — you send the three responses to it and ask which is best. This is a starter-tier version of an "LLM-as-judge" pattern that later courses (CLD-AI-107 RAG evaluation, CLD-AI-112 capstone) build on.
- **Results write to `results/`** which is `.gitignore`d — every run generates a fresh CSV timestamped in the filename. The point is watching the numbers move as you rerun, not persisting them.
