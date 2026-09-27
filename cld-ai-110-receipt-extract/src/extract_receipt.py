"""Extract a receipt to JSON via tool_use."""

import base64, json, os, sys
from dotenv import load_dotenv
import anthropic

load_dotenv()

img_path = sys.argv[1] if len(sys.argv) > 1 else "receipt.png"
with open(img_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

media = "image/png" if img_path.endswith(".png") else "image/jpeg"

tools = [{
    "name": "record_receipt",
    "description": "Record a structured receipt.",
    "input_schema": {
        "type": "object",
        "properties": {
            "merchant": {"type": ["string", "null"]},
            "date": {"type": ["string", "null"], "description": "YYYY-MM-DD"},
            "total": {"type": ["number", "null"]},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "desc": {"type": "string"},
                        "qty": {"type": "integer"},
                        "price": {"type": "number"}
                    }
                }
            }
        },
        "required": ["merchant", "total"]
    }
}]

client = anthropic.Anthropic()
r = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=2048,
    tools=tools,
    tool_choice={"type": "tool", "name": "record_receipt"},
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": media, "data": img_b64}},
            {"type": "text", "text": "Extract this receipt. For unreadable fields, use null."}
        ]
    }]
)

tool_call = next(b for b in r.content if b.type == "tool_use")
print(json.dumps(tool_call.input, indent=2))
