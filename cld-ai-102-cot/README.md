# CLD-AI-102 Lesson 6 — Apply chain-of-thought vs adaptive thinking

Starter for the third hands-on lab in the **Prompt Engineering with Claude** course. You take Orion Analytics' escalation-decision prompt, run it three ways (no reasoning surface, explicit chain-of-thought, adaptive thinking on Opus 5.5), measure accuracy + cost + latency across 15 escalation-shape tickets, and pick a production configuration based on your own numbers.

## Scenario

You're the junior engineer at **Orion Analytics**. Your few-shot triage classifier from L4 is at 95%. Now the escalation decisions — data loss / security keywords / regulatory acronyms — are wrong ~35% of the time on the compliance-adjacent tickets. Team lead asked you to test reasoning strategies from L5 on the escalation shape and recommend a production configuration.

## Files

```
cld-ai-102-cot/
  README.md                       # this file
  .env.example                    # ANTHROPIC_API_KEY (injected by lab proxy) + ANTHROPIC_MODEL default
  .gitignore                      # .env, __pycache__, .venv
  requirements.txt                # Manifest only — packages already installed in the lab container.
  data/
    escalation_tickets.json       # 15 escalation-shape tickets with Escalate/NoEscalate labels
  src/
    verify_env.py                 # Smoke test.
    escalate_no_reasoning.py      # Zero-shot baseline (COMPLETE, do not edit) — ~65% accuracy.
    escalate_cot.py               # Exercise 2 skeleton — TODO: add explicit <thinking> CoT.
    escalate_adaptive.py          # Exercise 3 skeleton — TODO: add output_config.effort on Opus 5.5.
    measure_reasoning.py          # Exercise 4 script — head-to-head accuracy + tokens + latency.
```

## How to run

The lab container ships the Anthropic SDK preinstalled + the Claude proxy wires `ANTHROPIC_API_KEY`. No `pip install`, no `cp .env`.

1. Terminal → New Terminal (opens at workspace root).
2. `python src/verify_env.py`.
3. Work through Exercises 1-4.

## What you'll practice

- **Explicit chain-of-thought** — adding `<thinking>...</thinking>` before `<decision>` for auditable reasoning.
- **Adaptive thinking** on Opus 5.5 — using `output_config.effort` for internal reasoning without changing the prompt.
- **Cost/latency vs accuracy tradeoff** — measuring all three approaches on the same 15 tickets and reading the three-way comparison.
- **The safe extraction pattern** (from L1) is now paying off THIRD time — adaptive thinking on Opus 5.5 always emits a ThinkingBlock; the same `next((b.text for b in resp.content if b.type == "text"), "")` filter handles it.

## Notes

- All model IDs from `ANTHROPIC_MODEL` env — never hardcoded.
- `output_config.effort` is 5.x-only. Old `thinking.budget_tokens` (4.x) is deprecated.
- Adaptive thinking bills THINKING tokens SEPARATELY from output tokens; the measure script reports both.
