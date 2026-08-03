# ai-3016-eval-sdk

Starter project for AI-3016 Lesson 16 — **Programmatic evaluation with the Azure AI Evaluation SDK**.

Runs the built-in Foundry evaluators (Groundedness, Relevance, Coherence, and Content Safety) plus one **custom evaluator** (citation accuracy) against a sample dataset of Aurora Insights consultant queries.

## What you'll build

- `src/run_eval.py` — the end-to-end evaluation harness. Calls Aurora's flow against a golden dataset, runs the evaluators, and prints an aggregate scorecard.
- `src/citation_accuracy.py` — a custom evaluator function you can extend.
- `data/golden.jsonl` — the sample evaluation dataset (20 rows).

## Prerequisites

- Aurora's `consulting-copilot-flow` deployed as an endpoint (lesson 8 + 11).
- `aurora-gpt-5-mini` (gpt-5-mini v2025-08-07, or another cheap deployment) available as the judge model.
- Environment variables from `.env.example`.

## Install

```bash
pip install -r requirements.txt
```

## Run

```bash
python src/run_eval.py
```

Expected output: per-row scores and aggregate scorecard printed to console; full results saved to `results/<timestamp>.json`.

## Extend

Add your own custom evaluator by copying the shape of `src/citation_accuracy.py` — a callable that takes `(question, response, context)` and returns a numeric score.
