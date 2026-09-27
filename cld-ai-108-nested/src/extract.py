"""Nested invoice extraction."""

import json, os, sys
from dotenv import load_dotenv
import anthropic


INVOICE_SCHEMA = {
    "name": "submit_invoice",
    "input_schema": {
        "type": "object",
        "properties": {
            "customer": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "tier": {"type": "string", "enum": ["Enterprise","Pro","Starter"]},
                },
                "required": ["id","name","tier"],
                "additionalProperties": False,
            },
            "invoice_date": {"type": "string"},
            "line_items": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "quantity": {"type": "integer", "minimum": 1},
                        "unit_price_usd": {"type": "number", "minimum": 0},
                    },
                    "required": ["description","quantity","unit_price_usd"],
                    "additionalProperties": False,
                },
            },
            "total_usd": {"type": "number", "minimum": 0},
        },
        "required": ["customer","invoice_date","line_items","total_usd"],
        "additionalProperties": False,
    }
}

SAMPLE_INVOICE = """
Invoice #INV-2026-9412
Customer: Acme Analytics Corp (id: acme-corp, tier: Enterprise)
Date: Sept 25, 2026

Items:
- 10 x Pro seats @ $99/mo = $990
- 3 x Extra data storage TB @ $50/mo = $150
- 1 x Priority support add-on @ $500/mo = $500

Total: $1,640.00
"""


def extract(client, model, invoice_text: str) -> dict:
    resp = client.messages.create(model=model, max_tokens=1024,
        tools=[INVOICE_SCHEMA],
        tool_choice={"type":"tool","name":"submit_invoice"},
        messages=[{"role":"user","content": f"Extract structured invoice from this text:\n\n{invoice_text}"}])
    return dict(next(b.input for b in resp.content if b.type == "tool_use"))


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    r = extract(client, model, SAMPLE_INVOICE)
    print(json.dumps(r, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
