"""Zero-shot baseline — no reasoning surface, DO NOT EDIT.

Complete. This is what your escalation prompt looks like BEFORE any
reasoning technique is added. `measure_reasoning.py` will call decide()
here as version 1 of 3.

Expected accuracy on data/escalation_tickets.json: ~60-70% on Sonnet 5.
The classifier gets the OBVIOUS triggers (T-3002 GDPR mention, T-3008
data loss) but misses the ambiguous ones (T-3011 http-instead-of-https
buried in a slow-dashboard complaint).

Run standalone: `python src/escalate_no_reasoning.py "ticket text..."`
"""

import json
import os
import sys
import time
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import anthropic


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


def decide(client: anthropic.Anthropic, model: str, ticket_text: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(ticket_text=ticket_text)
    t0 = time.perf_counter()
    resp = client.messages.create(
        model=model, max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    latency_ms = int((time.perf_counter() - t0) * 1000)

    text = next((b.text for b in resp.content if b.type == "text"), "")

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
        "thinking_tokens": 0,  # no adaptive thinking on this version
        "latency_ms": latency_ms,
        "model": model,
    }


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: escalate_no_reasoning.py \"<ticket text>\"", file=sys.stderr)
        return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    print(json.dumps(decide(client, model, sys.argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
