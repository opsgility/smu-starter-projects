"""Exercise 3 — run v1 and v2 across every ticket in data/tickets.json
and print the parse-failure-rate comparison table.

This is a runner, not a skeleton — it's complete when you fill in the
two TODOs in triage_v2_xml.py. If v2 is still stubbed you'll see 100%
parse-fail on the v2 column, which is the correct message that TODOs
are pending.

Run: `python src/measure_parse_rate.py`
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

# Import the two classify() implementations from their respective modules.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from triage_v1_unstructured import classify as classify_v1  # noqa: E402
from triage_v2_xml import classify as classify_v2  # noqa: E402


TICKETS_PATH = Path(__file__).resolve().parent.parent / "data" / "tickets.json"


def main() -> int:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()

    tickets = json.loads(TICKETS_PATH.read_text(encoding="utf-8"))
    print(f"measure_parse_rate: {len(tickets)} tickets x 2 versions = "
          f"{len(tickets) * 2} calls against model={model}\n")

    v1_parsed = 0
    v2_parsed = 0
    v1_category_correct = 0
    v2_category_correct = 0

    print(f"{'ID':<8} {'expected':<18} {'v1 parse':<12} {'v1 cat':<20} {'v2 parse':<12} {'v2 cat':<20}")
    print("-" * 92)

    for t in tickets:
        v1 = classify_v1(client, model, t["text"])
        v2 = classify_v2(client, model, t["text"])

        v1_ok = v1["parse_ok"]
        v2_ok = v2["parse_ok"]
        v1_cat = (v1.get("category") or "").strip() or "-"
        v2_cat = (v2.get("category") or "").strip() or "-"

        if v1_ok:
            v1_parsed += 1
            if v1_cat.lower() == t["expected_category"].lower():
                v1_category_correct += 1
        if v2_ok:
            v2_parsed += 1
            if v2_cat.lower() == t["expected_category"].lower():
                v2_category_correct += 1

        print(f"{t['id']:<8} {t['expected_category']:<18} "
              f"{'OK' if v1_ok else 'FAIL':<12} {v1_cat[:18]:<20} "
              f"{'OK' if v2_ok else 'FAIL':<12} {v2_cat[:18]:<20}")

    n = len(tickets)
    print("\nSummary:")
    print(f"  v1 (unstructured): parse_ok={v1_parsed}/{n} ({100*v1_parsed/n:.0f}%)  "
          f"category_correct_of_parsed={v1_category_correct}/{max(v1_parsed,1)}")
    print(f"  v2 (XML-tagged):   parse_ok={v2_parsed}/{n} ({100*v2_parsed/n:.0f}%)  "
          f"category_correct_of_parsed={v2_category_correct}/{max(v2_parsed,1)}")

    # A healthy v2 result on Sonnet 5 is 10/10 (100%) parse_ok — see README.
    return 0


if __name__ == "__main__":
    sys.exit(main())
