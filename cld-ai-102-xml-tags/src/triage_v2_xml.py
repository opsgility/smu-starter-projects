"""Exercise 2 — rewrite the triage prompt with XML tags.

Fill in the two TODOs below. The tests you'll run in Exercise 3
compare v1 (regex + fallback) against v2 (this file's `<category>` /
`<next_step>` output tags parsed with xml.etree). Aim to keep v2's
implementation under 30 lines of real code — the point is that XML
tags collapse the whole "parse a Claude reply" job into a one-liner.

Shape you're building toward:
- INPUT SEPARATION: wrap the ticket in `<ticket>...</ticket>` tags so
  Claude reads it as content-to-analyze, not instructions-to-follow.
- OUTPUT SHAPING: ask Claude to reply inside `<category>...</category>`
  and `<next_step>...</next_step>` tags, and NOTHING outside those.
- Parse with `xml.etree.ElementTree.fromstring(f"<r>{text}</r>")` —
  synthetic <r> root because Claude replies with two sibling tags at
  the top level and xml.etree needs a single root.

Run: `python src/triage_v2_xml.py "some ticket text..."`
     Prints a JSON row identical in shape to v1 so measure_parse_rate.py
     can compare the two head-to-head.
"""

import json
import os
import sys
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import anthropic


# TODO 1: write the XML-tagged version of the triage prompt.
# Requirements:
#   - Wrap the ticket text in <ticket>...</ticket> tags.
#   - Instruct Claude to reply inside <category>...</category> and
#     <next_step>...</next_step> tags AND NOTHING OUTSIDE those tags.
#   - Keep the four allowed categories (Billing, Technical, Feature
#     Request, Other).
# HINT: the shape should look roughly like:
#   """Classify the ticket below.
#
#   <ticket>
#   {ticket_text}
#   </ticket>
#
#   Reply inside <category>...</category> and <next_step>...</next_step>
#   tags only. Categories: Billing, Technical, Feature Request, Other."""
PROMPT_TEMPLATE = "TODO: replace this stub with the XML-tagged prompt."


def classify(client: anthropic.Anthropic, model: str, ticket_text: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(ticket_text=ticket_text)
    resp = client.messages.create(
        model=model,
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )

    # Safe text extraction (from CLD-AI-101 — adaptive-thinking models
    # may prepend a ThinkingBlock; the pattern below works for every model):
    text = next((b.text for b in resp.content if b.type == "text"), "")

    # TODO 2: parse `text` using xml.etree.ElementTree.
    #   - Wrap `text` in a synthetic <r>...</r> root before parsing, because
    #     Claude replies with two sibling top-level tags (<category> and
    #     <next_step>) and xml.etree.ElementTree.fromstring needs exactly
    #     one root element.
    #   - Extract `category` from root.find("category").text.strip()
    #   - Extract `next_step` from root.find("next_step").text.strip()
    #   - Set parse_ok = True on a clean parse, False on ET.ParseError OR
    #     when either tag is missing (root.find returns None).
    #
    # HINT: skeleton
    #   try:
    #       root = ET.fromstring(f"<r>{text}</r>")
    #       cat_elem = root.find("category")
    #       step_elem = root.find("next_step")
    #       if cat_elem is None or step_elem is None:
    #           return {"category": None, "next_step": None, "raw_reply": text, "parse_ok": False}
    #       return {
    #           "category": (cat_elem.text or "").strip(),
    #           "next_step": (step_elem.text or "").strip(),
    #           "raw_reply": text,
    #           "parse_ok": True,
    #       }
    #   except ET.ParseError:
    #       return {"category": None, "next_step": None, "raw_reply": text, "parse_ok": False}
    return {
        "category": None,
        "next_step": None,
        "raw_reply": text,
        "parse_ok": False,
    }


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: triage_v2_xml.py \"<ticket text>\"", file=sys.stderr)
        return 2

    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    result = classify(client, model, sys.argv[1])
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
