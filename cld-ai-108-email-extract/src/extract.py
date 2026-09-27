"""Extract structured email records via tool_use schema."""

import json, os, sys
from pathlib import Path
from dotenv import load_dotenv
import anthropic


SCHEMA = {
    "name": "submit_email_record",
    "input_schema": {
        "type": "object",
        "properties": {
            "sender": {"type": "string"},
            "intent": {"type": "string", "enum": ["support_request","renewal","feature_request","cancellation","compliance","other"]},
            "urgency": {"type": "string", "enum": ["urgent","normal","low"]},
            "deadline": {"type": ["string", "null"], "description": "ISO-ish date or short phrase like 'by Fri', null if none"},
            "action_items": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["sender","intent","urgency","deadline","action_items"],
        "additionalProperties": False,
    }
}


def extract(client, model, email_text: str) -> dict:
    """TODO: use tool_use pattern to extract structured record.
    HINT:
      resp = client.messages.create(model=model, max_tokens=1024,
          tools=[SCHEMA], tool_choice={"type":"tool","name":"submit_email_record"},
          messages=[{"role":"user","content": f"Extract fields:\\n\\n{email_text}"}])
      return dict(next(b.input for b in resp.content if b.type == "tool_use"))
    """
    raise NotImplementedError("TODO")


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    emails = json.loads((Path(__file__).resolve().parent.parent / "data" / "emails.json").read_text())
    for e in emails:
        print(f"\n=== {e['id']} ===")
        try:
            r = extract(client, model, e["text"])
        except NotImplementedError as ex:
            print(f"TODO: {ex}"); return 1
        print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
