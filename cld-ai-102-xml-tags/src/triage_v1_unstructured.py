"""Orion Analytics' L5-era triage prompt — reference version, DO NOT EDIT.

This is the prompt you're about to REPLACE. It works ~60% of the time and
that's the whole problem. It's here for the parse-rate comparison in
Exercise 3.

Shape:
- No input tags around the ticket text.
- No output shape — Claude replies in free-form prose.
- Downstream parser hunts for `Category:` with a regex + fallback.

Run: `python src/triage_v1_unstructured.py "some ticket text..."`
     Prints a JSON row: {"category": "...", "next_step": "...", "parse_ok": bool}
"""

import json
import os
import re
import sys

from dotenv import load_dotenv
import anthropic


PROMPT_TEMPLATE = """Classify this support ticket into one of Billing, Technical,
Feature Request, or Other, and suggest one specific next step.

{ticket_text}"""


# Realistic-fragile regex: accepts "Category:" / "Classification:" / "Class:" —
# matches Claude's common phrasings for zero-shot classification but still
# misses conversational replies like "This is a technical issue."
CATEGORY_REGEX = re.compile(
    r"(?:Category|Classification|Class)\s*[:\-]\s*\*{0,2}([A-Za-z ]+?)\*{0,2}(?:[\.\n\r]|$)",
    re.IGNORECASE,
)
NEXT_STEP_REGEX = re.compile(
    r"(?:Next\s*Step|Suggested\s*Next\s*Step|Recommendation|Action)\s*[:\-]\s*\*{0,2}(.+?)\*{0,2}(?:\n|$)",
    re.IGNORECASE,
)


def classify(client: anthropic.Anthropic, model: str, ticket_text: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(ticket_text=ticket_text)
    resp = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    text = next((b.text for b in resp.content if b.type == "text"), "")

    cat_match = CATEGORY_REGEX.search(text)
    step_match = NEXT_STEP_REGEX.search(text)

    parse_ok = cat_match is not None and step_match is not None

    return {
        "category": cat_match.group(1).strip() if cat_match else None,
        "next_step": step_match.group(1).strip() if step_match else None,
        "raw_reply": text,
        "parse_ok": parse_ok,
    }


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: triage_v1_unstructured.py \"<ticket text>\"", file=sys.stderr)
        return 2

    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    result = classify(client, model, sys.argv[1])
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
