# Lesson 10 evaluation wrapper. Runs Relevance + Groundedness + Fluency
# evaluators from azure.ai.evaluation over the golden JSONL and prints averages.
from __future__ import annotations

import json
import os
import statistics
import sys
from pathlib import Path

from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential

from azure.ai.evaluation import (
    FluencyEvaluator,
    GroundednessEvaluator,
    RelevanceEvaluator,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
GOLDEN_PATH = REPO_ROOT / "data" / "halcyon-eval-golden.jsonl"


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value or value.startswith("<"):
        print(f"[eval_runner] Missing env var: set this variable in .env -> {name}")
        sys.exit(1)
    return value


def load_records(path: Path) -> list[dict]:
    if not path.exists():
        print(
            f"[eval_runner] {path} not found. Run capture_golden.py first "
            f"during Lesson 10."
        )
        sys.exit(1)
    records = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))
    return records


def _score(evaluator, record: dict, uses_context: bool) -> float | None:
    """Call one evaluator on one record and pull the numeric score field."""
    kwargs = {"query": record["query"], "response": record["response"]}
    if uses_context:
        kwargs["context"] = record.get("context", "")
    result = evaluator(**kwargs)
    for key, value in result.items():
        if isinstance(value, (int, float)) and key.endswith("_score"):
            return float(value)
    return None


def main() -> None:
    load_dotenv()

    endpoint = require_env("AZURE_AI_PROJECT_ENDPOINT")
    deployment = require_env("AZURE_AI_CHAT_DEPLOYMENT")

    # The evaluators need a model config so they can call an LLM judge.
    # DefaultAzureCredential-backed inference on the Foundry project.
    model_config = {
        "azure_endpoint": endpoint,
        "azure_deployment": deployment,
        "api_version": "2024-10-21",
    }

    credential = DefaultAzureCredential()

    relevance = RelevanceEvaluator(model_config=model_config, credential=credential)
    groundedness = GroundednessEvaluator(model_config=model_config, credential=credential)
    fluency = FluencyEvaluator(model_config=model_config, credential=credential)

    records = load_records(GOLDEN_PATH)
    scores = {"relevance": [], "groundedness": [], "fluency": []}

    for record in records:
        r = _score(relevance, record, uses_context=False)
        g = _score(groundedness, record, uses_context=True)
        f = _score(fluency, record, uses_context=False)
        if r is not None:
            scores["relevance"].append(r)
        if g is not None:
            scores["groundedness"].append(g)
        if f is not None:
            scores["fluency"].append(f)
        print(f"[eval_runner] {record['query'][:60]} -> R={r} G={g} F={f}")

    print("[eval_runner] --- aggregate ---")
    for name, values in scores.items():
        if values:
            avg = statistics.mean(values)
            print(f"[eval_runner] {name:>12}: mean={avg:.3f}  n={len(values)}")
        else:
            print(f"[eval_runner] {name:>12}: no scores")


if __name__ == "__main__":
    main()
