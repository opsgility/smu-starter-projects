"""Exercise 3 — Custom LLM-as-judge for Ridgevault's regulatory-tone rubric.

Loads `data/rubrics/regulatory-tone.md`, sends it to `FOUNDRY_MODEL` as a
judge prompt against each row of `data/eval-results-builtin.jsonl` (from
Exercise 2), and writes per-row rubric scores to
`data/eval-results-regtone.jsonl`.

TODO (exercise): fill in `run_judge` — build the judge prompt, call the model
with `response_format={"type": "json_object"}`, parse the returned JSON, and
enforce that `total == sum(dimensions)`.
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path
from statistics import mean

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

RUBRIC = Path(__file__).resolve().parents[2] / "data" / "rubrics" / "regulatory-tone.md"
BUILTIN_RESULTS = Path(__file__).resolve().parents[2] / "data" / "eval-results-builtin.jsonl"
JUDGE_RESULTS = Path(__file__).resolve().parents[2] / "data" / "eval-results-regtone.jsonl"

DIMENSIONS = (
    "no_forward_looking_guarantees",
    "unqualified_performance_discipline",
    "advice_boundary_discipline",
    "client_appropriate_framing",
)


def run_judge(project: AIProjectClient, model: str, rubric_text: str, response_under_review: str) -> dict:
    """TODO(exercise 3): implement the judge call.

    Requirements:
      - Build a judge prompt that includes RUBRIC + RESPONSE.
      - Call the model with response_format={"type": "json_object"}.
      - Return the parsed JSON with the four dimension scores + total + rationale.
      - Enforce that total == sum of the four dimensions; if not, raise ValueError.
    """
    raise NotImplementedError("Fill this in per exercise 3.")


def main() -> int:
    load_dotenv()
    if not BUILTIN_RESULTS.exists():
        print(f"ERROR: run exercise 2 first — {BUILTIN_RESULTS} is missing.", file=sys.stderr)
        return 1

    project = AIProjectClient(
        endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )
    model = os.environ["FOUNDRY_MODEL"]
    rubric_text = RUBRIC.read_text(encoding="utf-8")

    scored: list[dict] = []
    for line in BUILTIN_RESULTS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        judgement = run_judge(project, model, rubric_text, row["response"])
        scored.append({"id": row["id"], "response": row["response"], **judgement})
        print(f"  {row['id']}: total={judgement.get('total')}")

    JUDGE_RESULTS.write_text("\n".join(json.dumps(s) for s in scored), encoding="utf-8")

    def avg(key: str) -> float:
        vals = [s[key] for s in scored if isinstance(s.get(key), (int, float))]
        return round(mean(vals), 2) if vals else float("nan")

    print()
    print("Aggregate rubric scores:")
    for dim in DIMENSIONS:
        print(f"  {dim}={avg(dim)}")
    print(f"  total={avg('total')}")
    print(f"Wrote {JUDGE_RESULTS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
