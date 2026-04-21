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
    # TODO (Exercise 3, Step 3): Retrieve top-5 chunks via retrieval.search(query, k=5)
    # TODO (Exercise 3, Step 3): Build context = "\n\n".join(
    #     f"[{h['source']}] {h['chunk']}" for h in hits)
    # TODO (Exercise 3, Step 3): Build prompt = f"Context:\n{context}\n\nQuestion: {query}"
    # TODO (Exercise 3, Step 3): Open an AIProjectClient (Foundry project endpoint +
    #     DefaultAzureCredential), then get_openai_client() and call
    #     client.responses.create(model=MODEL_DEPLOYMENT, input=[system, user])
    #     where the system prompt forces citation-only answers from the context.
    # TODO (Exercise 3, Step 3): Return {"response": r.output_text, "context": context}
    raise NotImplementedError("Exercise 3: implement chat_target()")


def main() -> None:
    """Run GroundednessEvaluator + RelevanceEvaluator against eval_data.jsonl."""
    # TODO (Exercise 3, Step 3): Read AZURE_AI_PROJECT_ENDPOINT + MODEL_DEPLOYMENT
    #     and build `model_config` with:
    #       azure_endpoint:   <project endpoint without /api/projects/...>
    #       azure_deployment: MODEL_DEPLOYMENT
    #       api_version:      "2024-10-21"
    # TODO (Exercise 3, Step 3): Call evaluate(
    #       data="eval_data.jsonl",
    #       target=chat_target,
    #       evaluators={
    #           "groundedness": GroundednessEvaluator(model_config),
    #           "relevance":    RelevanceEvaluator(model_config),
    #       },
    #       evaluator_config={
    #           "groundedness": {"column_mapping": {
    #               "query":    "${data.query}",
    #               "response": "${outputs.response}",
    #               "context":  "${outputs.context}",
    #           }},
    #           "relevance": {"column_mapping": {
    #               "query":    "${data.query}",
    #               "response": "${outputs.response}",
    #           }},
    #       },
    #       azure_ai_project=<AZURE_AI_PROJECT_ENDPOINT>,
    #       output_path="./eval_output.json",
    #     )
    # TODO (Exercise 3, Step 3): Print result["studio_url"] and result["metrics"].
    raise NotImplementedError("Exercise 3: implement main()")


if __name__ == "__main__":
    main()
