"""Exercise 2 — Foundry built-in evaluators over the portfolio-review test set.

Runs Relevance + Groundedness + Coherence from `azure.ai.evaluation` over the
12 rows in `data/test-set-portfolio-reviews.jsonl` and writes per-row scores +
aggregate averages to `data/eval-results-builtin.jsonl`.

Env: FOUNDRY_PROJECT_ENDPOINT + FOUNDRY_MODEL from .env.
Auth: DefaultAzureCredential (Foundry User + Cognitive Services OpenAI User).
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path
from statistics import mean

from azure.ai.evaluation import (
    CoherenceEvaluator,
    GroundednessEvaluator,
    RelevanceEvaluator,
)
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

TEST_SET = Path(__file__).resolve().parents[2] / "data" / "test-set-portfolio-reviews.jsonl"
RESULTS = Path(__file__).resolve().parents[2] / "data" / "eval-results-builtin.jsonl"


def build_model_config() -> dict:
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model = os.environ["FOUNDRY_MODEL"]
    # The evaluator SDK accepts an AzureOpenAIModelConfiguration-shaped dict.
    # azure_endpoint here is the Foundry account endpoint (parent of /api/projects/*).
    account_endpoint = endpoint.split("/api/projects/")[0]
    return {
        "azure_endpoint": account_endpoint,
        "azure_deployment": model,
        "api_version": "2025-04-01-preview",
    }


def load_test_set() -> list[dict]:
    return [json.loads(line) for line in TEST_SET.read_text(encoding="utf-8").splitlines() if line.strip()]


def generate_response(project: AIProjectClient, model: str, row: dict) -> str:
    """Use the deployed model to produce the Portfolio Analyst reply we then score."""
    openai_client = project.get_openai_client(api_version="2025-04-01-preview")
    resp = openai_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Ridgevault Financial's Portfolio Analyst. Answer using ONLY the CONTEXT "
                    "below. Keep replies to 2-4 sentences."
                ),
            },
            {"role": "user", "content": f"CONTEXT:\n{row['context']}\n\nQUESTION: {row['query']}"},
        ],
        max_completion_tokens=300,
    )
    return (resp.choices[0].message.content or "").strip()


def main() -> int:
    load_dotenv()
    if "FOUNDRY_PROJECT_ENDPOINT" not in os.environ or "FOUNDRY_MODEL" not in os.environ:
        print("ERROR: set FOUNDRY_PROJECT_ENDPOINT + FOUNDRY_MODEL in .env first.", file=sys.stderr)
        return 1

    project = AIProjectClient(
        endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )
    model_config = build_model_config()
    relevance = RelevanceEvaluator(model_config)
    groundedness = GroundednessEvaluator(model_config)
    coherence = CoherenceEvaluator(model_config)

    rows = load_test_set()
    print(f"Running built-in evaluators over {len(rows)} test cases...")

    results: list[dict] = []
    for row in rows:
        response = generate_response(project, os.environ["FOUNDRY_MODEL"], row)
        rel = relevance(query=row["query"], response=response)
        gnd = groundedness(response=response, context=row["context"])
        coh = coherence(query=row["query"], response=response)
        results.append({
            "id": row["id"],
            "query": row["query"],
            "response": response,
            "relevance": rel.get("relevance"),
            "groundedness": gnd.get("groundedness"),
            "coherence": coh.get("coherence"),
        })
        print(f"  {row['id']}: rel={rel.get('relevance')} gnd={gnd.get('groundedness')} coh={coh.get('coherence')}")

    RESULTS.write_text("\n".join(json.dumps(r) for r in results), encoding="utf-8")

    def avg(key: str) -> float:
        vals = [r[key] for r in results if isinstance(r.get(key), (int, float))]
        return round(mean(vals), 2) if vals else float("nan")

    print()
    print(f"Aggregate: relevance={avg('relevance')} groundedness={avg('groundedness')} coherence={avg('coherence')}")
    print(f"Wrote {RESULTS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
