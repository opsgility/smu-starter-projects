"""Exercise 2 — extract structured records via tool_use.

Fill in the TODO to call Claude with the schema-tool + tool_choice pattern
from L7 Topic 1 Beat 2, then return block.input as the extraction dict.

Run standalone: `python src/extract.py "some ticket text"`
"""

import json
import os
import sys

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, os.path.dirname(__file__))
from schemas import STRICT_SCHEMA


def extract(client: anthropic.Anthropic, model: str, ticket_text: str,
            schema: dict = STRICT_SCHEMA) -> dict:
    """Return the schema-validated extraction dict, or {'_error': str} on failure."""
    # TODO: call client.messages.create() with:
    #   model=model, max_tokens=1024
    #   tools=[schema]
    #   tool_choice={"type": "tool", "name": schema["name"]}
    #   messages=[{"role":"user","content": f"Extract structured fields from this ticket:\n{ticket_text}"}]
    #
    # Then find the tool_use block in response.content and return block.input.
    #
    # HINT:
    #   response = client.messages.create(
    #       model=model, max_tokens=1024,
    #       tools=[schema],
    #       tool_choice={"type": "tool", "name": schema["name"]},
    #       messages=[{"role": "user",
    #                  "content": f"Extract structured fields from this ticket:\n{ticket_text}"}],
    #   )
    #   tool_block = next((b for b in response.content if b.type == "tool_use"), None)
    #   if tool_block is None:
    #       return {"_error": "Claude did not emit a tool_use block"}
    #   return dict(tool_block.input)
    raise NotImplementedError("TODO: implement extract()")


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: extract.py \"<ticket text>\""); return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    result = extract(client, model, sys.argv[1])
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
