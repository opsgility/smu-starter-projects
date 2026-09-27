"""Exercise 3 — extract 15 tickets and validate every record.

Runs the STRICT and LOOSE schemas across the 15 tickets, checks whether
each extraction is warehouse-ready (all required fields present, enums
respected, entities well-formed), and reports the failure rate per schema.

Run: `python src/validate.py`
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract import extract
from schemas import STRICT_SCHEMA, LOOSE_SCHEMA


REQUIRED_FIELDS = ["customer_id", "category", "sentiment", "requires_escalation",
                  "recommended_action", "entities"]
VALID_CATEGORIES = {"Billing", "Technical", "Feature Request", "Escalate", "Other"}
VALID_SENTIMENTS = {"positive", "neutral", "negative", "urgent"}
VALID_ENTITY_TYPES = {"customer_id", "product", "amount_usd", "date", "regulatory_keyword", "endpoint"}


def validate_record(rec: dict) -> list[str]:
    """Return list of validation errors (empty = valid)."""
    if "_error" in rec:
        return [f"extraction error: {rec['_error']}"]
    errors = []
    for f in REQUIRED_FIELDS:
        if f not in rec:
            errors.append(f"missing field '{f}'")
    if rec.get("category") not in VALID_CATEGORIES:
        errors.append(f"invalid category '{rec.get('category')}'")
    if rec.get("sentiment") not in VALID_SENTIMENTS:
        errors.append(f"invalid sentiment '{rec.get('sentiment')}'")
    if not isinstance(rec.get("requires_escalation"), bool):
        errors.append(f"requires_escalation not boolean")
    if not isinstance(rec.get("entities"), list):
        errors.append("entities not a list")
    else:
        for i, e in enumerate(rec["entities"]):
            if not isinstance(e, dict):
                errors.append(f"entities[{i}] not a dict"); continue
            if e.get("type") not in VALID_ENTITY_TYPES:
                errors.append(f"entities[{i}].type='{e.get('type')}' not in enum")
            if not isinstance(e.get("value"), str):
                errors.append(f"entities[{i}].value not string")
    return errors


def main() -> int:
    load_dotenv()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()

    tickets_path = Path(__file__).resolve().parent.parent / "data" / "tickets.json"
    tickets = json.loads(tickets_path.read_text(encoding="utf-8"))

    print(f"validate: {len(tickets)} tickets x 2 schemas against model={model}\n")

    for schema_name, schema in [("STRICT", STRICT_SCHEMA), ("LOOSE", LOOSE_SCHEMA)]:
        print(f"\n{'='*70}\n{schema_name} schema\n{'='*70}")
        valid_count = 0
        for t in tickets:
            try:
                rec = extract(client, model, t["text"], schema=schema)
            except NotImplementedError as e:
                print(f"  {t['id']}: TODO not filled ({e})")
                continue
            errors = validate_record(rec)
            if not errors:
                valid_count += 1
                print(f"  {t['id']}: ✓ valid  category={rec.get('category')}  "
                      f"sentiment={rec.get('sentiment')}  entities={len(rec.get('entities',[]))}")
            else:
                print(f"  {t['id']}: ✗ INVALID  errors={errors[:3]}")
        n = len(tickets)
        print(f"\n  {schema_name} summary: {valid_count}/{n} valid ({100*valid_count/max(n,1):.0f}%)")

    print("\nExpected pattern:")
    print("  STRICT: 15/15 valid (100%) — every field constrained by enums+required")
    print("  LOOSE:  0-5/15 valid (0-33%) — Claude fills in random shapes without schema guidance")
    return 0


if __name__ == "__main__":
    sys.exit(main())
