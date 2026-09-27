"""Exercise 4 — accuracy head-to-head across zero-shot / few-shot / bad-few-shot.

Runs all 20 tickets from data/tickets.json against three classifiers:
  1. triage_zero_shot (L2's v2 — baseline)
  2. triage_few_shot (Exercise 2 — well-chosen edge-case examples)
  3. triage_few_shot_bad (Exercise 3 — all-Billing ablation)

Total: 60 Claude calls, ~2-4 min wall clock.

Prints a table per ticket + summary block per version. The expected pattern:
  zero-shot     ~85% accuracy
  few-shot      ~95%+ accuracy (well-chosen examples LIFT)
  bad-few-shot  ~70-78% accuracy (bad examples DROP below zero-shot)

Run: `python src/measure_accuracy.py`
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from triage_zero_shot import classify as classify_zero  # noqa: E402
from triage_few_shot import classify as classify_few  # noqa: E402
from triage_few_shot_bad import classify as classify_bad  # noqa: E402


TICKETS_PATH = Path(__file__).resolve().parent.parent / "data" / "tickets.json"


def _accuracy_row(correct: int, total: int) -> str:
    pct = 100 * correct / max(total, 1)
    return f"{correct}/{total} ({pct:.0f}%)"


def main() -> int:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()

    tickets = json.loads(TICKETS_PATH.read_text(encoding="utf-8"))
    typical = [t for t in tickets if t.get("kind") == "typical"]
    edges = [t for t in tickets if t.get("kind") == "edge_case"]
    print(f"measure_accuracy: {len(tickets)} tickets ({len(typical)} typical + {len(edges)} edge_case) x "
          f"3 versions = {len(tickets) * 3} calls against model={model}\n")

    versions = [
        ("zero-shot", classify_zero),
        ("few-shot", classify_few),
        ("bad-few-shot", classify_bad),
    ]

    # Skip a version if its module's example list is empty (TODOs not filled).
    def is_ready(name: str) -> bool:
        if name == "few-shot":
            from triage_few_shot import FEW_SHOT_EXAMPLES  # noqa: F811
            return bool(FEW_SHOT_EXAMPLES)
        if name == "bad-few-shot":
            from triage_few_shot_bad import BAD_EXAMPLES  # noqa: F811
            return bool(BAD_EXAMPLES)
        return True

    results: dict[str, list[dict]] = {name: [] for name, _ in versions}

    header = f"{'ID':<8} {'kind':<10} {'expected':<18} " + " ".join(
        f"{name[:14]:<15}" for name, _ in versions
    )
    print(header)
    print("-" * len(header))

    for t in tickets:
        row_parts = [f"{t['id']:<8}", f"{t['kind']:<10}", f"{t['expected_category']:<18}"]
        for name, fn in versions:
            if not is_ready(name):
                row_parts.append(f"{'(skip)':<15}")
                results[name].append({"parse_ok": False, "category": None, "correct": False, "ticket": t})
                continue
            r = fn(client, model, t["text"])
            cat = (r.get("category") or "").strip()
            correct = cat.lower() == t["expected_category"].lower()
            results[name].append({**r, "correct": correct, "ticket": t})
            row_parts.append(f"{('✓' if correct else '✗') + ' ' + cat[:13]:<15}")
        print(" ".join(row_parts))

    print("\nSummary — category correctness:")
    for name, _ in versions:
        rows = results[name]
        if not any(r["parse_ok"] for r in rows):
            print(f"  {name:<15}: (skipped — module TODO not filled in)")
            continue
        overall = sum(r["correct"] for r in rows)
        overall_str = _accuracy_row(overall, len(rows))
        typ_rows = [r for r in rows if r["ticket"]["kind"] == "typical"]
        edge_rows = [r for r in rows if r["ticket"]["kind"] == "edge_case"]
        typ_str = _accuracy_row(sum(r["correct"] for r in typ_rows), len(typ_rows))
        edge_str = _accuracy_row(sum(r["correct"] for r in edge_rows), len(edge_rows))
        print(f"  {name:<15}: overall={overall_str}   typical={typ_str}   edge={edge_str}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
