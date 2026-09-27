"""Exercise 4 — the Improver-polished version.

Paste the improved prompt from the Anthropic Prompt Improver Playground
into the constants below. The API-call shape stays IDENTICAL to v3 (same
system arg, same messages arg, same XML tag parsing) — only the CONTENT
of SYSTEM_PROMPT + PROMPT_TEMPLATE + FEW_SHOT_EXAMPLES changes.

If the Improver returned a monolithic prompt (no separate system/user
split), put the whole thing in PROMPT_TEMPLATE and leave SYSTEM_PROMPT
as a short role-only sentence.

Target accuracy on data/tickets.json: ~95-99% on Sonnet 5.

Run standalone: `python src/triage_v4_improved.py "ticket text..."`
"""

import json
import os
import sys
import xml.etree.ElementTree as ET

from dotenv import load_dotenv
import anthropic


# TODO 1 — paste the Improver's system prompt here.
SYSTEM_PROMPT = "TODO: paste Improver-refined system prompt."


# TODO 2 — paste the Improver's few-shot examples here (may be more or
# fewer than v3's 3; the Improver often picks a different count).
FEW_SHOT_EXAMPLES: list[dict] = []


def _format_examples(examples: list[dict]) -> str:
    if not examples:
        return ""
    blocks = []
    for ex in examples:
        # If the Improver returned raw XML text per example, use it directly.
        if "raw_xml" in ex:
            blocks.append(ex["raw_xml"])
            continue
        blocks.append(
            f"<example>\n"
            f"  <input>{ex['input']}</input>\n"
            f"  <output>\n"
            f"    <thinking>{ex.get('thinking', '[reasoning]')}</thinking>\n"
            f"    <category>{ex['output']['category']}</category>\n"
            f"    <next_step>{ex['output']['next_step']}</next_step>\n"
            f"  </output>\n"
            f"</example>"
        )
    return "\n\n".join(blocks) + "\n\n"


# TODO 3 — paste the Improver's user-turn template here.
# Must include {examples_block} and {ticket_text} format placeholders.
PROMPT_TEMPLATE = "TODO: paste Improver-refined user prompt template."


def classify(client: anthropic.Anthropic, model: str, ticket_text: str) -> dict:
    prompt = PROMPT_TEMPLATE.format(
        examples_block=_format_examples(FEW_SHOT_EXAMPLES),
        ticket_text=ticket_text,
    )
    resp = client.messages.create(
        model=model, max_tokens=1000,
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
        print("usage: triage_v4_improved.py \"<ticket text>\"", file=sys.stderr)
        return 2
    if SYSTEM_PROMPT.startswith("TODO") or PROMPT_TEMPLATE.startswith("TODO"):
        print("v4: TODOs unfilled — paste the Improver-refined prompt content.", file=sys.stderr)
        return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    print(json.dumps(classify(anthropic.Anthropic(), model, sys.argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
