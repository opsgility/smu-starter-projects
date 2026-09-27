"""Exercise 3 — build the Anthropic Prompt Improver test set.

Reads data/test_set_seed.json (8 rows) and asks you to expand to 15 by
adding 5-7 more rows drawn from data/tickets.json — targeting the
buckets you want the Improver to optimize against most.

Outputs the final test set as BOTH JSONL and CSV to results/, so you
can copy-paste either format into the Improver Playground.

Fill in the TODO with the additional row IDs from data/tickets.json.

Run: `python src/build_test_set.py`
"""

import csv
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SEED_PATH = ROOT / "data" / "test_set_seed.json"
TICKETS_PATH = ROOT / "data" / "tickets.json"
RESULTS_DIR = ROOT / "results"


# TODO: add 5-7 ticket IDs from data/tickets.json to expand the seed
# test set to ~15 rows total. Pick from the edge + adversarial buckets
# for maximum Improver signal.
# Suggestions (why each is a good add):
#   C-4013: snippy one-liner Other — currently hard for classifier
#   C-4017: ambiguous bug-or-docs Technical
#   C-4018: mixed intent (primary Billing, secondary Feature Request)
#   C-4019: urgency signal that shouldn't shift category
#   C-4021: buried security in tech ticket
#   C-4024: instruction-shaped ticket (adversarial)
#   C-4025: XML-like content in ticket body (adversarial)
ADDITIONAL_TICKET_IDS: list[str] = []


def main() -> int:
    seed = json.loads(SEED_PATH.read_text(encoding="utf-8"))
    tickets = json.loads(TICKETS_PATH.read_text(encoding="utf-8"))

    if not ADDITIONAL_TICKET_IDS:
        print("build_test_set: ADDITIONAL_TICKET_IDS is empty.", file=sys.stderr)
        print("  Fill in the TODO with 5-7 ticket IDs from data/tickets.json.", file=sys.stderr)
        return 2

    ticket_by_id = {t["id"]: t for t in tickets}

    rows = list(seed["rows"])
    for tid in ADDITIONAL_TICKET_IDS:
        t = ticket_by_id.get(tid)
        if t is None:
            print(f"build_test_set: unknown ticket ID '{tid}' — skipping.", file=sys.stderr)
            continue
        rows.append({"input": t["text"], "expected": t["expected_category"]})

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    jsonl_path = RESULTS_DIR / "improver_test_set.jsonl"
    with jsonl_path.open("w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    csv_path = RESULTS_DIR / "improver_test_set.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["input", "expected"])
        w.writeheader()
        w.writerows(rows)

    print(f"build_test_set: wrote {len(rows)} rows to")
    print(f"  {jsonl_path}")
    print(f"  {csv_path}")
    print("\nNext step: open https://platform.claude.com/prompt-improver in your browser.")
    print("Paste your v3 prompt from src/triage_v3_engineered.py (SYSTEM_PROMPT +")
    print("PROMPT_TEMPLATE with an example ticket_text) into the Prompt Improver.")
    print("Upload one of the files above as the test set. Set the rubric to")
    print("\"category exact match to `expected`\". Click Improve. Copy the")
    print("improved prompt back into src/triage_v4_improved.py (Exercise 4).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
