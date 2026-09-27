"""Exercise 3 — the "bad examples" ablation.

Fill in the TODO with 3 ALL-BILLING examples (deliberately bad selection).
This is the ablation from L3 Topic 2 Beat 5 — you're proving to yourself
that BAD examples DROP accuracy below zero-shot, not just fail to help.

Aim: category accuracy DROPS to ~70-78% on the 20 tickets in
data/tickets.json — worse than zero-shot's ~85%. The classifier will
over-classify things as "Billing" because that's what the examples
demonstrated.

This is a critical production intuition: example COUNT is not the point;
example SELECTION is.

Run standalone: `python src/triage_few_shot_bad.py "ticket text..."`
"""

import json
import os
import sys
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import anthropic


# TODO: replace the empty list with 3 examples ALL LABELED "Billing".
# Pick 3 real-shape Billing tickets — they can be well-worded and
# grammatically clean. The point is that they're monolithic in category.
# HINT: skeleton
#   BAD_EXAMPLES = [
#       {
#           "input": "Charged twice for September renewal — please refund duplicate.",
#           "output": {
#               "category": "Billing",
#               "next_step": "Verify duplicate charge and process refund within 3 business days.",
#           },
#       },
#       {
#           "input": "How do I add three more users this quarter? Admin says I'm at plan limit.",
#           "output": {
#               "category": "Billing",
#               "next_step": "Upgrade plan seat limit and confirm the change in the customer's admin panel.",
#           },
#       },
#       {
#           "input": "Cancelling my subscription effective end of billing cycle. Please confirm.",
#           "output": {
#               "category": "Billing",
#               "next_step": "Confirm cancellation, disable auto-renew, and email a final invoice on cycle end.",
#           },
#       },
#   ]
BAD_EXAMPLES: list[dict] = []


def _format_examples(examples: list[dict]) -> str:
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
        examples_block=_format_examples(BAD_EXAMPLES),
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
        print("usage: triage_few_shot_bad.py \"<ticket text>\"", file=sys.stderr)
        return 2
    if not BAD_EXAMPLES:
        print("triage_few_shot_bad: BAD_EXAMPLES is empty — fill in the TODO before running.",
              file=sys.stderr)
        return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    print(json.dumps(classify(client, model, sys.argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
