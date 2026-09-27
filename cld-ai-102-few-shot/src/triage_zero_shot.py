"""L2's v2 XML-tagged classifier — complete, DO NOT EDIT.

Zero-shot baseline. Ships from L2 as-is. Instructions + XML input/output tags,
no examples. `measure_accuracy.py` will call classify() here as one of three
head-to-head versions.

Expected accuracy on the 20 tickets in data/tickets.json: ~85-88% category
correctness (parse rate should be ~100% thanks to output tags).

Run standalone: `python src/triage_zero_shot.py "ticket text..."`
"""

import json
import os
import sys
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import anthropic


PROMPT_TEMPLATE = """You are a support-triage helper for Orion Analytics.
Classify the ticket below into one of Billing, Technical, Feature Request, or Other,
and suggest one specific next step.

<ticket>
{ticket_text}
</ticket>

Reply inside <category>...</category> and <next_step>...</next_step> tags only.
Do not include anything outside those tags."""


def classify(client: anthropic.Anthropic, model: str, ticket_text: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(ticket_text=ticket_text)
    resp = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    text = next((b.text for b in resp.content if b.type == "text"), "")

    try:
        root = ET.fromstring(f"<r>{text}</r>")
        cat = root.find("category")
        step = root.find("next_step")
        if cat is None or step is None:
            return {"category": None, "next_step": None, "raw_reply": text, "parse_ok": False}
        return {
            "category": (cat.text or "").strip(),
            "next_step": (step.text or "").strip(),
            "raw_reply": text,
            "parse_ok": True,
        }
    except ET.ParseError:
        return {"category": None, "next_step": None, "raw_reply": text, "parse_ok": False}


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: triage_zero_shot.py \"<ticket text>\"", file=sys.stderr)
        return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    print(json.dumps(classify(client, model, sys.argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
