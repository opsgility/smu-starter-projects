"""Exercise 5 — full accuracy trajectory across all versions.

Runs 25 tickets against every non-stub version (v0 always; v3 if TODOs
filled; v4 if TODOs filled) and prints per-ticket + summary accuracy
broken down by kind (typical / edge / adversarial).

~50-75 Claude calls, ~3-6 min wall clock on Sonnet 5.

Run: `python src/measure_all.py`
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from triage_v0_broken import classify as cls_v0  # noqa: E402
from triage_v3_engineered import (  # noqa: E402
    classify as cls_v3,
    SYSTEM_PROMPT as V3_SYS,
    FEW_SHOT_EXAMPLES as V3_EX,
    PROMPT_TEMPLATE as V3_TMPL,
)
from triage_v4_improved import (  # noqa: E402
    classify as cls_v4,
    SYSTEM_PROMPT as V4_SYS,
    PROMPT_TEMPLATE as V4_TMPL,
)


TICKETS_PATH = Path(__file__).resolve().parent.parent / "data" / "tickets.json"


def _accuracy(rows: list[dict]) -> str:
    n = len(rows)
    correct = sum(r["_correct"] for r in rows)
    return f"{correct}/{n} ({100*correct/max(n,1):.0f}%)"


def _accuracy_by_kind(rows: list[dict], kind: str) -> str:
    subset = [r for r in rows if r["_ticket"]["kind"] == kind]
    return _accuracy(subset) if subset else "-"


def main() -> int:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()

    tickets = json.loads(TICKETS_PATH.read_text(encoding="utf-8"))

    v3_ready = (not V3_SYS.startswith("TODO")) and V3_EX and (not V3_TMPL.startswith("TODO"))
    v4_ready = (not V4_SYS.startswith("TODO")) and (not V4_TMPL.startswith("TODO"))

    versions = [("v0-broken", cls_v0, True)]
    versions.append(("v3-engineered", lambda c, m, t: cls_v3(c, m, t), v3_ready))
    versions.append(("v4-improved", lambda c, m, t: cls_v4(c, m, t), v4_ready))

    active = [(n, f) for n, f, r in versions if r]
    skipped = [n for n, _, r in versions if not r]

    n_calls = len(tickets) * len(active)
    print(f"measure_all: {len(tickets)} tickets x {len(active)} versions = {n_calls} calls "
          f"against model={model}")
    if skipped:
        print(f"  Skipped (TODOs not filled): {', '.join(skipped)}")
    print()

    all_results: dict[str, list[dict]] = {n: [] for n, _, _ in versions}

    header = f"{'ID':<8} {'kind':<12} {'expected':<18} " + " ".join(
        f"{n[:14]:<15}" for n, _, r in versions
    )
    print(header)
    print("-" * len(header))

    for t in tickets:
        parts = [f"{t['id']:<8}", f"{t['kind']:<12}", f"{t['expected_category']:<18}"]
        for name, fn, ready in versions:
            if not ready:
                parts.append(f"{'(skip)':<15}")
                all_results[name].append({"_correct": False, "_ticket": t, "category": None})
                continue
            r = fn(client, model, t["text"])
            cat = (r.get("category") or "").strip().lower()
            correct = cat == t["expected_category"].lower()
            r["_correct"] = correct
            r["_ticket"] = t
            all_results[name].append(r)
            parts.append(f"{('✓' if correct else '✗') + ' ' + (r.get('category') or 'FAIL')[:12]:<15}")
        print(" ".join(parts))

    print("\nSummary — accuracy by kind:")
    for name, _, ready in versions:
        rows = all_results[name]
        if not ready:
            print(f"  {name:<15}: (skipped)")
            continue
        overall = _accuracy(rows)
        typ = _accuracy_by_kind(rows, "typical")
        edge = _accuracy_by_kind(rows, "edge")
        adv = _accuracy_by_kind(rows, "adversarial")
        print(f"  {name:<15}: overall={overall}   typical={typ}   edge={edge}   adversarial={adv}")

    print("\nExpected trajectory:")
    print("  v0-broken       : overall ~72-78%    (edge is weakest)")
    print("  v3-engineered   : overall ~90-95%    (edge jumps most; adversarial gets neutralized by <ticket> tags)")
    print("  v4-improved     : overall ~95-99%    (Improver squeezes the final tail on ambiguous cases)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
