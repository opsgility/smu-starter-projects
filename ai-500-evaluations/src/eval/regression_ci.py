"""Exercise 6 — Plug the evaluators into a mini CI-style regression run.

Reads the latest `data/eval-results-builtin.jsonl` + `data/eval-results-regtone.jsonl`,
compares aggregate scores against `data/ci-baseline.json` (creating it on the
first run), and exits non-zero if any dimension regressed by more than the
allowed delta. This is the pattern a real CI job would run per pull request.

Env: FOUNDRY_PROJECT_ENDPOINT + FOUNDRY_MODEL from .env (read by the
   upstream evaluators; this script itself does not call the model).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path
from statistics import mean

BUILTIN = Path(__file__).resolve().parents[2] / "data" / "eval-results-builtin.jsonl"
REGTONE = Path(__file__).resolve().parents[2] / "data" / "eval-results-regtone.jsonl"
BASELINE = Path(__file__).resolve().parents[2] / "data" / "ci-baseline.json"

# Any dimension score that drops by more than this fails the regression gate.
ALLOWED_DELTA = 0.5

DIMENSIONS = (
    "relevance",
    "groundedness",
    "coherence",
    "no_forward_looking_guarantees",
    "unqualified_performance_discipline",
    "advice_boundary_discipline",
    "client_appropriate_framing",
    "total",
)


def _avg(rows: list[dict], key: str) -> float | None:
    vals = [r[key] for r in rows if isinstance(r.get(key), (int, float))]
    return round(mean(vals), 3) if vals else None


def _load(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    if not BUILTIN.exists() or not REGTONE.exists():
        print(
            "ERROR: run exercise 2 (run_builtin_evaluators) AND exercise 3 (regulatory_tone_judge) first.",
            file=sys.stderr,
        )
        return 2

    builtin_rows = _load(BUILTIN)
    regtone_rows = _load(REGTONE)

    current = {}
    for dim in ("relevance", "groundedness", "coherence"):
        current[dim] = _avg(builtin_rows, dim)
    for dim in (
        "no_forward_looking_guarantees",
        "unqualified_performance_discipline",
        "advice_boundary_discipline",
        "client_appropriate_framing",
        "total",
    ):
        current[dim] = _avg(regtone_rows, dim)

    if not BASELINE.exists():
        BASELINE.write_text(json.dumps(current, indent=2), encoding="utf-8")
        print(f"BASELINE not present — wrote first baseline to {BASELINE}.")
        for dim in DIMENSIONS:
            print(f"  {dim} = {current[dim]}")
        return 0

    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    regressions: list[str] = []
    print("Regression report (baseline -> current):")
    for dim in DIMENSIONS:
        b = baseline.get(dim)
        c = current.get(dim)
        if b is None or c is None:
            print(f"  {dim}: skipped (missing)")
            continue
        delta = round(c - b, 3)
        marker = "  "
        if delta < -ALLOWED_DELTA:
            marker = "!!"
            regressions.append(f"{dim} regressed by {delta:+.3f} (allowed: {ALLOWED_DELTA})")
        print(f"  {marker} {dim}: {b} -> {c} ({delta:+.3f})")

    if regressions:
        print()
        print("FAIL — regressions detected:")
        for r in regressions:
            print(f"  - {r}")
        return 1

    print()
    print("PASS — no regressions above the allowed delta.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
