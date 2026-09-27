"""Exercise 2 — add cache_control markers on the stable content.

Fill in the TWO TODOs to route the same content through the API in a
CACHE-OPTIMIZED shape. Instead of sending everything as one monolithic
user-content string, you'll:

  1. Send SYSTEM_PROMPT as a list-shape system parameter with a
     cache_control marker (though SYSTEM_PROMPT alone is only ~80 tokens,
     so this marker below the 1024-token minimum won't actually cache —
     kept as a demo of the API shape).
  2. Send EXAMPLES_BLOCK as its own text block in messages[0].content
     WITH a cache_control marker — this block IS above the 1024-token
     minimum and WILL cache-hit on the second call within the 5-minute
     TTL.
  3. Send the per-call ticket text as a separate text block WITHOUT
     cache_control.

Expected cache metrics after Exercise 4:
  - First call (cold): cache_creation_input_tokens ~= EXAMPLES_BLOCK size (~1500 tokens)
  - Subsequent calls: cache_read_input_tokens ~= EXAMPLES_BLOCK size, cache_creation ~= 0

Run standalone: `python src/classify_cached.py "ticket text..."`
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
    # TODO 1: build the `system` argument as a LIST of typed content blocks
    # (not a plain string). One block with type "text", the SYSTEM_PROMPT
    # text, and cache_control: {"type": "ephemeral"}.
    #
    # HINT: skeleton
    #   system_arg = [
    #       {
    #           "type": "text",
    #           "text": SYSTEM_PROMPT,
    #           "cache_control": {"type": "ephemeral"},
    #       }
    #   ]
    system_arg = SYSTEM_PROMPT  # <-- replace with the list-shape

    # TODO 2: build the messages argument. messages[0].content should be a
    # LIST of two typed blocks:
    #   Block A: the EXAMPLES_BLOCK with cache_control on it. This is the
    #     one that actually gets cached (it's above 1024 tokens).
    #   Block B: the per-call ticket wrapped in <ticket> tags. NO cache_control.
    #
    # HINT: skeleton
    #   messages_arg = [
    #       {
    #           "role": "user",
    #           "content": [
    #               {
    #                   "type": "text",
    #                   "text": EXAMPLES_BLOCK,
    #                   "cache_control": {"type": "ephemeral"},
    #               },
    #               {
    #                   "type": "text",
    #                   "text": f"Now classify the ticket below:\n<ticket>\n{ticket_text}\n</ticket>",
    #               },
    #           ],
    #       }
    #   ]
    messages_arg = [{"role": "user", "content": f"{EXAMPLES_BLOCK}\n\nClassify:\n<ticket>\n{ticket_text}\n</ticket>"}]

    resp = client.messages.create(
        model=model,
        max_tokens=500,
        system=system_arg,
        messages=messages_arg,
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
        print("usage: classify_cached.py \"<ticket text>\"", file=sys.stderr)
        return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    print(json.dumps(classify(client, model, sys.argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
