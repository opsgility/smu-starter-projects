"""Exercise 2 — apply L1 XML tags + L4 few-shot + L6 CoT all together.

Fill in the THREE TODOs to layer every prompt-engineering technique from
CLD-AI-102 into ONE prompt. This is the "engineered" tier — the input to
the Prompt Improver in Exercise 3.

Target accuracy on data/tickets.json: ~90-95% on Sonnet 5.

Run standalone: `python src/triage_v3_engineered.py "ticket text..."`
"""

import json
import os
import sys
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import anthropic


# TODO 1 — write the SYSTEM PROMPT.
# It should establish the role (Orion Analytics support-triage helper),
# list the 4 categories, and state the reply-only-inside-tags rule.
#
# HINT:
#   SYSTEM_PROMPT = """You are a support-triage helper for Orion Analytics.
#   Classify each ticket into one of: Billing, Technical, Feature Request, Other.
#   Reply inside <thinking>...</thinking>, <category>...</category>, and
#   <next_step>...</next_step> tags only. Do not include anything outside those tags."""
SYSTEM_PROMPT = "TODO: replace this stub with a real system prompt."


# TODO 2 — build the FEW_SHOT_EXAMPLES list (L4-style).
# 3 examples, edge-case-covering. Suggested selections drawn from
# data/tickets.json's edge bucket:
#   - Cancellation-with-feature-gap → Feature Request (C-4011 shape)
#   - Technical-with-billing-hint → Technical (C-4012 shape)
#   - Downgrade-with-satisfaction-note → Billing (C-4016 shape)
#
# HINT:
#   FEW_SHOT_EXAMPLES = [
#       {"input": "Cancelling my subscription. Would stay if you supported SSO/SAML — that's the real blocker.",
#        "output": {"category": "Feature Request", "next_step": "Log SSO/SAML request in product backlog and flag as churn-risk in CRM."}},
#       ...
#   ]
FEW_SHOT_EXAMPLES: list[dict] = []


def _format_examples(examples: list[dict]) -> str:
    if not examples:
        return ""
    blocks = []
    for ex in examples:
        blocks.append(
            f"<example>\n"
            f"  <input>{ex['input']}</input>\n"
            f"  <output>\n"
            f"    <thinking>[example reasoning: which category and why]</thinking>\n"
            f"    <category>{ex['output']['category']}</category>\n"
            f"    <next_step>{ex['output']['next_step']}</next_step>\n"
            f"  </output>\n"
            f"</example>"
        )
    return "\n\n".join(blocks) + "\n\n"


# TODO 3 — write the PROMPT_TEMPLATE that stacks L1 tags + L4 examples + L6 CoT.
# Required shape:
#   Instructions (recall from system prompt via the model).
#   Few-shot examples block (from _format_examples).
#   The new ticket wrapped in <ticket>...</ticket>.
#   Instruction to reason inside <thinking>...</thinking> first, then produce
#   <category> and <next_step>.
#
# HINT:
#   PROMPT_TEMPLATE = """Here are examples of the classification pattern:
#
#   {examples_block}Classify the ticket below. First reason inside
#   <thinking>...</thinking> tags (identify primary intent, note any secondary
#   asks), then produce your final answer inside <category>...</category> and
#   <next_step>...</next_step> tags.
#
#   <ticket>
#   {ticket_text}
#   </ticket>"""
PROMPT_TEMPLATE = "TODO: replace this stub with the L1+L4+L6 stacked prompt."


def classify(client: anthropic.Anthropic, model: str, ticket_text: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(
        examples_block=_format_examples(FEW_SHOT_EXAMPLES),
        ticket_text=ticket_text,
    )
    resp = client.messages.create(
        model=model, max_tokens=1000,  # headroom for <thinking>
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    text = next((b.text for b in resp.content if b.type == "text"), "")

    try:
        root = ET.fromstring(f"<r>{text}</r>")
        cat = root.find("category")
        step = root.find("next_step")
        thinking = root.find("thinking")
        return {
            "category": (cat.text or "").strip() if cat is not None else None,
            "next_step": (step.text or "").strip() if step is not None else None,
            "thinking": (thinking.text or "").strip() if thinking is not None else None,
            "raw_reply": text,
            "parse_ok": cat is not None and step is not None,
        }
    except ET.ParseError:
        return {"category": None, "next_step": None, "thinking": None,
                "raw_reply": text, "parse_ok": False}


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: triage_v3_engineered.py \"<ticket text>\"", file=sys.stderr)
        return 2
    if SYSTEM_PROMPT.startswith("TODO"):
        print("v3: SYSTEM_PROMPT stub — fill in TODO 1.", file=sys.stderr); return 2
    if not FEW_SHOT_EXAMPLES:
        print("v3: FEW_SHOT_EXAMPLES empty — fill in TODO 2.", file=sys.stderr); return 2
    if PROMPT_TEMPLATE.startswith("TODO"):
        print("v3: PROMPT_TEMPLATE stub — fill in TODO 3.", file=sys.stderr); return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    print(json.dumps(classify(anthropic.Anthropic(), model, sys.argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
