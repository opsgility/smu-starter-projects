"""Exercise 2 — layer 3 well-chosen few-shot examples on top of the L2 prompt.

Fill in the TODO below. Your job: hand-pick 3 examples that address the
Orion classifier's known confusion patterns (cancellation-with-features,
technical-with-billing-hint, snippy one-liners). L3 Beat 3 walked exactly
this selection with a worked example.

Aim: category accuracy jumps from ~85% (zero-shot in triage_zero_shot.py)
to ~95%+ on the 20 tickets in data/tickets.json (measured by
measure_accuracy.py in Exercise 4).

Run standalone: `python src/triage_few_shot.py "ticket text..."`
"""

import json
import os
import sys
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import anthropic


# TODO: replace the empty examples list with 3 hand-picked few-shot examples.
# Requirements:
#   - Each example is a dict with "input" (the ticket text) and "output"
#     (a dict with "category" and "next_step").
#   - Pick EDGE CASES from the confusion patterns, NOT typical tickets.
#     Suggested selections (drawn from L3 Beat 3):
#       1. Cancellation-with-feature-gap → Feature Request
#       2. Technical-with-billing-hint → Technical
#       3. A clear Billing ticket for grounding.
#   - The three examples together should teach Claude: "classify on the
#     underlying issue, not the surface phrasing."
#
# HINT: skeleton
#   FEW_SHOT_EXAMPLES = [
#       {
#           "input": "Cancelling my subscription. Would stay if you added SSO/SAML — that's the real blocker.",
#           "output": {
#               "category": "Feature Request",
#               "next_step": "Log SSO/SAML request in product backlog and flag as churn-risk in CRM.",
#           },
#       },
#       {
#           "input": "We're hitting 429 rate-limit errors on /v2/analytics pushing us into overage on our bill. Please help.",
#           "output": {
#               "category": "Technical",
#               "next_step": "Investigate 429 source on /v2/analytics; loop in billing for overage credit if root cause is our end.",
#           },
#       },
#       {
#           "input": "Charged twice for September renewal — see attached statement. Please refund duplicate.",
#           "output": {
#               "category": "Billing",
#               "next_step": "Verify duplicate charge and process refund within 3 business days.",
#           },
#       },
#   ]
FEW_SHOT_EXAMPLES: list[dict] = []


def _format_examples(examples: list[dict]) -> str:
    """Render the examples list as an <example>...</example> block sequence."""
    if not examples:
        return ""
    blocks = []
    for ex in examples:
        blocks.append(
            f"<example>\n"
            f"  <input>{ex['input']}</input>\n"
            f"  <output>\n"
            f"    <category>{ex['output']['category']}</category>\n"
            f"    <next_step>{ex['output']['next_step']}</next_step>\n"
            f"  </output>\n"
            f"</example>"
        )
    return "\n\n".join(blocks) + "\n\n"


PROMPT_TEMPLATE = """You are a support-triage helper for Orion Analytics.
Classify the ticket into one of Billing, Technical, Feature Request, or Other,
and suggest one specific next step.

Here are examples of the classification pattern:

{examples_block}Now classify the ticket below:
<ticket>
{ticket_text}
</ticket>

Reply inside <category>...</category> and <next_step>...</next_step> tags only.
Do not include anything outside those tags."""


def classify(client: anthropic.Anthropic, model: str, ticket_text: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(
        examples_block=_format_examples(FEW_SHOT_EXAMPLES),
        ticket_text=ticket_text,
    )
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
        print("usage: triage_few_shot.py \"<ticket text>\"", file=sys.stderr)
        return 2
    if not FEW_SHOT_EXAMPLES:
        print("triage_few_shot: FEW_SHOT_EXAMPLES is empty — fill in the TODO before running.",
              file=sys.stderr)
        return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    print(json.dumps(classify(client, model, sys.argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
