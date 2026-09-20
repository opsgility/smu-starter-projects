"""Foundry Evaluations harness for the Summitline Outfitters RAG pipeline.

Exercise 3, Step 3 asks you to implement `chat_target()` and `main()`. The
evaluation reads `eval_data.jsonl` (one query per row), invokes `chat_target`
for each query, and scores the results with `GroundednessEvaluator` and
`RelevanceEvaluator`.

Run with:

    python -m app.evaluate
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

from azure.ai.evaluation import (
    GroundednessEvaluator,
    RelevanceEvaluator,
    evaluate,
)

from app import retrieval  # noqa: F401  (kept so target fns can import alongside)

load_dotenv()


def chat_target(query: str) -> dict:
    """End-to-end RAG call used by `evaluate()` for every eval row.

    Must return a plain dict with exactly two keys so the evaluator
    `column_mapping` values (`${outputs.response}` and `${outputs.context}`)
    resolve:

        {"response": "<model answer>", "context": "<retrieved chunks>"}
    """
    # Exercise 3 - Step 3 Start
    raise NotImplementedError("Complete Exercise 3 Step 3")
    # Exercise 3 - Step 3 End


def main() -> None:
    """Run GroundednessEvaluator + RelevanceEvaluator against eval_data.jsonl."""
    # Exercise 3 - Step 3 Start
    raise NotImplementedError("Complete Exercise 3 Step 3")
    # Exercise 3 - Step 3 End


if __name__ == "__main__":
    main()
