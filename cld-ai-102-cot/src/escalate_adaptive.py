"""Exercise 3 — use adaptive thinking on Claude Opus 5.5.

Fill in the TODO to pass output_config.effort on the API call. Prompt
stays SIMPLE (no <thinking> tags asked for) — Opus handles the reasoning
internally.

This version pins model="claude-opus-5-5" in code (regardless of
ANTHROPIC_MODEL) because adaptive thinking is most interesting on Opus.

Run standalone: `python src/escalate_adaptive.py "ticket text..."`
"""

import json
import os
import sys
import time
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import anthropic


# Same shape as escalate_no_reasoning — no <thinking> instruction; Opus reasons internally.
PROMPT_TEMPLATE = """You are the escalation-decision helper for Orion Analytics.
Decide whether this ticket needs Escalation. Escalation triggers:
  - Data loss / data corruption reports
  - Security keywords (breach, unauthorized access, exposure, incident, PII leak)
  - Regulatory acronyms (GDPR, HIPAA, SOC 2, PCI, CCPA)
Any one trigger present → Escalate. None → NoEscalate.

<ticket>
{ticket_text}
</ticket>

Reply inside <decision>Escalate | NoEscalate</decision> tags only.
Do not include anything outside those tags."""


# TODO: fill in this constant to enable adaptive thinking on Opus 5.5.
# The value must be a dict with an "effort" key mapping to one of
# "minimal", "low", "medium", "high". For an escalation decision use
# "high" — it's a multi-condition combination that benefits from deep
# reasoning.
#
# HINT: OUTPUT_CONFIG = {"effort": "high"}
OUTPUT_CONFIG: dict = {}


def decide(client: anthropic.Anthropic, ticket_text: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(ticket_text=ticket_text)
    t0 = time.perf_counter()
    kwargs = {
        "model": "claude-opus-5-5",  # pinned — adaptive thinking is Opus's story
        "max_tokens": 2000,
        "messages": [{"role": "user", "content": prompt}],
    }
    if OUTPUT_CONFIG:
        kwargs["output_config"] = OUTPUT_CONFIG
    resp = client.messages.create(**kwargs)
    latency_ms = int((time.perf_counter() - t0) * 1000)

    # ThinkingBlock is emitted before TextBlock — the same safe extraction
    # pattern from L1 handles this. WITHOUT this filter Opus 5.5 crashes
    # any code that assumes response.content[0].text.
    text = next((b.text for b in resp.content if b.type == "text"), "")

    # If the SDK exposes thinking tokens, capture them. Attribute name has
    # varied across SDK versions — fall back to 0 if not present.
    thinking_tokens = 0
    for attr in ("thinking_tokens", "output_thinking_tokens"):
        if hasattr(resp.usage, attr):
            thinking_tokens = getattr(resp.usage, attr) or 0
            break

    try:
        root = ET.fromstring(f"<r>{text}</r>")
        dec = root.find("decision")
        decision = (dec.text or "").strip() if dec is not None else None
        parse_ok = dec is not None
    except ET.ParseError:
        decision, parse_ok = None, False

    return {
        "decision": decision,
        "raw_reply": text,
        "parse_ok": parse_ok,
        "input_tokens": resp.usage.input_tokens,
        "output_tokens": resp.usage.output_tokens,
        "thinking_tokens": thinking_tokens,
        "latency_ms": latency_ms,
        "model": "claude-opus-5-5",
    }


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: escalate_adaptive.py \"<ticket text>\"", file=sys.stderr)
        return 2
    if not OUTPUT_CONFIG:
        print("escalate_adaptive: OUTPUT_CONFIG is empty — fill in the TODO with {'effort': 'high'}.",
              file=sys.stderr)
        return 2
    client = anthropic.Anthropic()
    print(json.dumps(decide(client, sys.argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
