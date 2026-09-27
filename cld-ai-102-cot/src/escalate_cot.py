"""Exercise 2 — add explicit <thinking> chain-of-thought.

Fill in the two TODOs to add a <thinking> reasoning surface before the
<decision> output tag. Same 15 tickets, same model (Sonnet 5 by default);
this exercise proves the ~65% → ~90% accuracy lift on Orion's escalation
decisions.

Run standalone: `python src/escalate_cot.py "ticket text..."`
"""

import json
import os
import sys
import time
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import anthropic


# TODO 1: rewrite PROMPT_TEMPLATE to add explicit chain-of-thought.
# Requirements:
#   - Keep the same escalation trigger list from escalate_no_reasoning.py.
#   - Keep the <ticket>...</ticket> input tag.
#   - Add an INSTRUCTION that asks Claude to reason inside
#     <thinking>...</thinking> tags BEFORE producing <decision>. The
#     reasoning should walk through the 3 trigger classes (data loss,
#     security keywords, regulatory acronyms), note whether the ticket
#     mentions anything in each, then combine into a final decision.
#   - Reply structure: <thinking>...</thinking>\n<decision>Escalate | NoEscalate</decision>
#
# HINT: skeleton
#   PROMPT_TEMPLATE = """You are the escalation-decision helper for Orion Analytics.
#   Decide whether this ticket needs Escalation. Escalation triggers:
#     - Data loss / data corruption reports
#     - Security keywords (breach, unauthorized access, exposure, incident, PII leak)
#     - Regulatory acronyms (GDPR, HIPAA, SOC 2, PCI, CCPA)
#   Any one trigger present → Escalate. None → NoEscalate.
#
#   <ticket>
#   {ticket_text}
#   </ticket>
#
#   First, reason through the decision inside <thinking>...</thinking> tags.
#   List each of the three trigger classes, note whether the ticket
#   mentions anything in that class, then combine into a final decision.
#
#   Then produce your final answer inside <decision>Escalate | NoEscalate</decision> tags."""
PROMPT_TEMPLATE = "TODO: rewrite this stub with the explicit chain-of-thought version."


def decide(client: anthropic.Anthropic, model: str, ticket_text: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(ticket_text=ticket_text)
    t0 = time.perf_counter()
    resp = client.messages.create(
        model=model,
        max_tokens=800,  # more headroom for <thinking> content
        messages=[{"role": "user", "content": prompt}],
    )
    latency_ms = int((time.perf_counter() - t0) * 1000)

    text = next((b.text for b in resp.content if b.type == "text"), "")

    # TODO 2: parse the reply. Extract BOTH the <thinking> text and the
    # <decision> text. Wrap in a synthetic <r>...</r> root before parsing
    # (same pattern as L2 for sibling top-level tags).
    #
    # HINT: skeleton
    #   try:
    #       root = ET.fromstring(f"<r>{text}</r>")
    #       thinking_elem = root.find("thinking")
    #       decision_elem = root.find("decision")
    #       if decision_elem is None:
    #           return {"decision": None, "thinking": None, "raw_reply": text, "parse_ok": False,
    #                   "input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens,
    #                   "thinking_tokens": 0, "latency_ms": latency_ms, "model": model}
    #       return {
    #           "decision": (decision_elem.text or "").strip(),
    #           "thinking": (thinking_elem.text or "").strip() if thinking_elem is not None else None,
    #           "raw_reply": text,
    #           "parse_ok": True,
    #           "input_tokens": resp.usage.input_tokens,
    #           "output_tokens": resp.usage.output_tokens,
    #           "thinking_tokens": 0,
    #           "latency_ms": latency_ms,
    #           "model": model,
    #       }
    #   except ET.ParseError:
    #       return {"decision": None, "thinking": None, "raw_reply": text, "parse_ok": False,
    #               "input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens,
    #               "thinking_tokens": 0, "latency_ms": latency_ms, "model": model}
    return {"decision": None, "thinking": None, "raw_reply": text, "parse_ok": False,
            "input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens,
            "thinking_tokens": 0, "latency_ms": latency_ms, "model": model}


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: escalate_cot.py \"<ticket text>\"", file=sys.stderr)
        return 2
    if PROMPT_TEMPLATE.startswith("TODO"):
        print("escalate_cot: PROMPT_TEMPLATE stub not replaced — fill in TODO 1.", file=sys.stderr)
        return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    print(json.dumps(decide(client, model, sys.argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
