"""Exercise 3 — DELIBERATELY break the cache with an upstream timestamp.

Fill in the TODO by prepending the current timestamp to the EXAMPLES_BLOCK
BEFORE the cache_control marker. This is the classic cache-miss failure
mode L7 Topic 2 Beat 6 warned about — a per-call value in the cached
portion invalidates the cache on every call.

You should see: cache_creation_input_tokens filled EVERY call (not just
first call); cache_read_input_tokens stays 0. Total cost ends up HIGHER
than the uncached baseline because you're paying the ~25% write surcharge
on every single call for no savings.

Run standalone: `python src/classify_cached_broken.py "ticket text..."`
"""

import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, os.path.dirname(__file__))
from _shared import SYSTEM_PROMPT, EXAMPLES_BLOCK


def classify(client: anthropic.Anthropic, model: str, ticket_text: str) -> dict:
    # TODO: build cached_block by concatenating a per-call timestamp
    # BEFORE the EXAMPLES_BLOCK. This is the anti-pattern — the timestamp
    # changes every call, so the byte content of cached_block is different
    # every call, so the cache misses every time.
    #
    # HINT:
    #   now = datetime.utcnow().isoformat(timespec="microseconds")
    #   cached_block = f"Timestamp: {now}\n\n{EXAMPLES_BLOCK}"
    #
    # (Yes, this is deliberately wrong. That's the point.)
    cached_block = EXAMPLES_BLOCK  # <-- replace with the timestamp+EXAMPLES_BLOCK form

    resp = client.messages.create(
        model=model,
        max_tokens=500,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": cached_block,
                        "cache_control": {"type": "ephemeral"},
                    },
                    {
                        "type": "text",
                        "text": f"Classify:\n<ticket>\n{ticket_text}\n</ticket>",
                    },
                ],
            }
        ],
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
        print("usage: classify_cached_broken.py \"<ticket text>\"", file=sys.stderr)
        return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    print(json.dumps(classify(client, model, sys.argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
