"""L4-style few-shot classifier with NO caching — DO NOT EDIT.

Baseline for the caching comparison. Sends system + examples + ticket
concatenated as a single user-content string. Cache_control absent. Every
call pays full input token cost.

Run standalone: `python src/classify_uncached.py "ticket text..."`
"""

import json
import os
import sys
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, os.path.dirname(__file__))
from _shared import SYSTEM_PROMPT, EXAMPLES_BLOCK


def classify(client: anthropic.Anthropic, model: str, ticket_text: str) -> dict:
    # Monolithic user-content string — no cache_control anywhere.
    user_content = (
        f"{EXAMPLES_BLOCK}\n\n"
        f"Now classify the ticket below:\n<ticket>\n{ticket_text}\n</ticket>"
    )
    resp = client.messages.create(
        model=model,
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )
    text = next((b.text for b in resp.content if b.type == "text"), "")

    try:
        root = ET.fromstring(f"<r>{text}</r>")
        cat = root.find("category")
        step = root.find("next_step")
        category = (cat.text or "").strip() if cat is not None else None
        next_step = (step.text or "").strip() if step is not None else None
        parse_ok = cat is not None and step is not None
    except ET.ParseError:
        category, next_step, parse_ok = None, None, False

    usage = resp.usage
    return {
        "category": category,
        "next_step": next_step,
        "parse_ok": parse_ok,
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0) or 0,
        "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", 0) or 0,
    }


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: classify_uncached.py \"<ticket text>\"", file=sys.stderr)
        return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    print(json.dumps(classify(client, model, sys.argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
