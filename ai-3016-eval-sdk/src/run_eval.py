"""AI-3016 Lesson 16 — programmatic evaluation with the Azure AI Evaluation SDK.

End-to-end harness:
  1. Load the golden dataset from data/golden.jsonl.
  2. For each row, call Aurora's deployed flow, capture response + context.
  3. Run built-in evaluators (Groundedness, Relevance, Coherence) + our
     custom citation_accuracy evaluator.
  4. Aggregate per-metric scores and print a scorecard.

Run once, tweak the flow, re-run — that's the CI/CD-friendly cycle.
"""

import os
import json
import time
import requests
from pathlib import Path
from datetime import datetime, timezone

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential

from azure.ai.evaluation import (
    GroundednessEvaluator,
    RelevanceEvaluator,
    CoherenceEvaluator,
)

from citation_accuracy import citation_accuracy


HERE = Path(__file__).parent
DATA_PATH = HERE.parent / "data" / "golden.jsonl"
RESULTS_DIR = HERE.parent / "results"


def load_golden() -> list[dict]:
    with DATA_PATH.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def call_flow(user_question: str) -> dict:
    endpoint = os.environ["AURORA_FLOW_ENDPOINT"]
    credential = DefaultAzureCredential()
    token = credential.get_token("https://ml.azure.com/.default").token
    resp = requests.post(
        endpoint,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"chat_history": [], "user_question": user_question},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def build_model_config() -> dict:
    return {
        "azure_endpoint": os.environ["JUDGE_OPENAI_ENDPOINT"].rsplit("/openai", 1)[0],
        "azure_deployment": os.environ["JUDGE_DEPLOYMENT"],
        "api_version": os.environ.get("JUDGE_API_VERSION", "2024-08-01-preview"),
    }


def run_row(row: dict, evaluators: dict) -> dict:
    q = row["question"]
    flow_out = call_flow(q)
    answer = flow_out.get("answer", "")
    sources = flow_out.get("sources", [])

    # Assemble the shape each built-in evaluator wants.
    context_text = "\n".join(
        s.get("content", "") for s in sources if s.get("content")
    ) or "no context retrieved"

    scores = {"question": q, "answer": answer}
    for name, ev in evaluators.items():
        try:
            r = ev(query=q, response=answer, context=context_text)
            # Built-in evaluators return dicts; keep the primary numeric value.
            main_key = next(iter(k for k in r if isinstance(r[k], (int, float))), name)
            scores[name] = r[main_key]
        except Exception as exc:  # pragma: no cover
            scores[name] = f"ERROR: {exc}"

    # Custom evaluator (deterministic, no LLM call).
    scores.update(citation_accuracy(response=answer, context=sources))
    return scores


def aggregate(rows: list[dict]) -> dict:
    """Mean of numeric columns, ignoring errors."""
    metrics = [k for k in rows[0] if isinstance(rows[0].get(k), (int, float))]
    agg = {}
    for m in metrics:
        vals = [r[m] for r in rows if isinstance(r.get(m), (int, float))]
        agg[m] = round(sum(vals) / len(vals), 3) if vals else None
    return agg


def main() -> None:
    load_dotenv()
    RESULTS_DIR.mkdir(exist_ok=True)

    model_config = build_model_config()
    evaluators = {
        "groundedness": GroundednessEvaluator(model_config=model_config),
        "relevance": RelevanceEvaluator(model_config=model_config),
        "coherence": CoherenceEvaluator(model_config=model_config),
    }

    dataset = load_golden()
    print(f"Loaded {len(dataset)} rows from {DATA_PATH.name}")

    rows_out = []
    for i, row in enumerate(dataset, 1):
        print(f"[{i}/{len(dataset)}] evaluating: {row['question'][:70]}...")
        rows_out.append(run_row(row, evaluators))

    agg = aggregate(rows_out)
    print("\n=== SCORECARD ===")
    for k, v in agg.items():
        print(f"  {k:24s} {v}")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    out_path = RESULTS_DIR / f"eval-{stamp}.json"
    out_path.write_text(json.dumps({"aggregate": agg, "rows": rows_out}, indent=2))
    print(f"\nFull results saved to {out_path.name}")


if __name__ == "__main__":
    main()
