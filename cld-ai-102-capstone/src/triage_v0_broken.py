"""Broken starter — DO NOT EDIT. This is the ~75% baseline the capstone improves on.

Deliberately made bad in three ways:
  1. No XML tags — ticket text pasted inline; output "just say the category" prose.
  2. No few-shot examples — pure zero-shot.
  3. No reasoning surface — no <thinking> tags, no adaptive thinking.

Parse strategy: split on "Category:" and hope. Fallback to None.

Expected accuracy on data/tickets.json: ~72-78% on Sonnet 5.
Expected parse rate: ~85-92% (some replies won't include the exact "Category:" string).

Run standalone: `python src/triage_v0_broken.py "ticket text..."`
"""

import json
import os
import re
import sys

from dotenv import load_dotenv
import anthropic


PROMPT_TEMPLATE = """Classify this support ticket for Orion Analytics. The categories
are Billing, Technical, Feature Request, or Other. Just say the category.

{ticket_text}"""


CATEGORY_REGEX = re.compile(r"(?:Category\s*:\s*)?(Billing|Technical|Feature Request|Other)",
                             re.IGNORECASE)


def classify(client: anthropic.Anthropic, model: str, ticket_text: str) -> dict:
    resp = client.messages.create(
        model=model, max_tokens=200,
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(ticket_text=ticket_text)}],
    )
    text = next((b.text for b in resp.content if b.type == "text"), "")
    match = CATEGORY_REGEX.search(text)
    return {
        "category": match.group(1).strip().title() if match else None,
        "raw_reply": text,
        "parse_ok": match is not None,
    }


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: triage_v0_broken.py \"<ticket text>\"", file=sys.stderr)
        return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    print(json.dumps(classify(anthropic.Anthropic(), model, sys.argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
