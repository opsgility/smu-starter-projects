# CLD-AI-102 Lesson 10 — Capstone: iterate a real Orion triage prompt through the Prompt Improver

Capstone hands-on for **Prompt Engineering with Claude**. You take a purposely-broken Orion Analytics classifier (~75% accuracy — no XML tags, no examples, no reasoning surface), rewrite it end-to-end applying L1 XML tags + L4 few-shot + L6 explicit CoT (climbing through ~85% → ~92% → ~95%), build a 15-row edge-covering test set for the Prompt Improver, run the improved prompt through the Anthropic Playground's Prompt Improver at `platform.claude.com`, paste the auto-refined prompt back, and measure the full accuracy trajectory head-to-head across all 5 versions.

## Scenario

Same Orion Analytics story that's threaded through CLD-AI-101 + all of CLD-AI-102. Your team lead is doing a mock code review of your CLD-AI-102 deliverable and wants to see the prompt-engineering ladder from ~75% (broken starter) to ~97% (Improver-polished final) with quantitative evidence at each step. This lab is that ladder.

## Files

```
cld-ai-102-capstone/
  README.md                    # this file
  .env.example                 # ANTHROPIC_API_KEY (injected) + ANTHROPIC_MODEL
  .gitignore                   # .env, __pycache__
  requirements.txt             # anthropic + python-dotenv (preinstalled)
  data/
    tickets.json               # 25 tickets: 10 typical + 12 edge + 3 adversarial
    test_set_seed.json         # 8-row starter test set for the Improver (student expands to 15)
  src/
    verify_env.py              # Smoke test.
    triage_v0_broken.py        # Broken starter (COMPLETE, do not edit) — ~75% accuracy.
    triage_v3_engineered.py    # Exercise 2 skeleton — TODO: apply L1 XML + L4 few-shot + L6 CoT.
    triage_v4_improved.py      # Exercise 4 skeleton — TODO: paste Improver output here.
    build_test_set.py          # Exercise 3 helper — output the JSON test set for the Improver.
    measure_all.py             # Exercise 5 runner — 25 tickets x 5 versions, accuracy trajectory.
```

## How to run

Standard: `python src/verify_env.py`, then work Exercises 1-5 in order.

## The 5-step accuracy ladder

| Version | Techniques | Expected accuracy on 25 tickets |
|---------|------------|--------------------------------|
| v0 (broken starter) | none | ~72-78% |
| v1 (implicit — v3 without CoT) | XML tags + few-shot | ~85-90% |
| v2 (implicit — v3 without few-shot) | XML tags + CoT | ~82-87% |
| v3 (engineered) | XML + few-shot + CoT | ~90-95% |
| v4 (Improver-polished) | v3 + Anthropic Prompt Improver | ~95-99% |

Only v0, v3, and v4 are testable via measure_all.py. v1 and v2 are conceptual intermediate steps mentioned in the accuracy table for context — the exercise sequence skips them for time.

## Prompt Improver access

The Anthropic Prompt Improver lives at:

**https://platform.claude.com/prompt-improver**

Sign in with any Claude Console account (free tier works). The Improver is a Playground feature, not a hosted-lab feature — you'll switch to your browser for Exercise 4 (paste prompt → paste test set → click Improve → copy improved prompt back to the lab container). The container itself doesn't need to reach the Improver programmatically; the copy-paste flow keeps this teachable without new tooling.

## What you'll practice

- Reading a broken prompt and identifying which techniques (L1 tags, L4 examples, L6 CoT) will move accuracy MOST.
- Stacking XML input/output tags + few-shot examples + explicit `<thinking>` CoT in ONE prompt.
- Building a 15-row test set spanning typical + edge + adversarial buckets.
- Feeding a prompt + test set into the Anthropic Prompt Improver via the Playground UI.
- Reading the Improver's diff and copying the improved prompt back into working Python.
- Measuring the full 5-version accuracy trajectory and defending the numbers in a mock code review.

## Notes

- Every model reference reads from `ANTHROPIC_MODEL` env — never hardcoded.
- Sonnet 5 recommended for the capstone measurements. Haiku 4.5 works but the deltas between versions are noisier.
- The Improver's Playground UI can accept the test set as JSONL or CSV. `build_test_set.py` outputs both formats.
- 5-version × 25-ticket run = 125 Claude calls, ~6-8 min wall clock on Sonnet 5.
