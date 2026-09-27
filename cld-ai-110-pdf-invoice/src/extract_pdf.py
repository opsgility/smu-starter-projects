"""Send a whole PDF to Claude and get structured extraction."""

import base64, json, os
from dotenv import load_dotenv
import anthropic

load_dotenv()

with open("invoice.pdf", "rb") as f:
    pdf_b64 = base64.b64encode(f.read()).decode()

client = anthropic.Anthropic()
r = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": [
            {"type": "document",
             "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_b64}},
            {"type": "text", "text": (
                "Summarize this invoice. Return JSON: "
                '{"invoice_id": str, "customer": str, "total": float, '
                '"line_items": [{"desc": str, "amount": float}], "due_date": str}. '
                "Reply with ONLY the JSON."
            )}
        ]
    }]
)

text = next((b.text for b in r.content if b.type == "text"), "")
data = json.loads(text.strip("`json \n"))
print(json.dumps(data, indent=2))
print(f"\n[input_tokens: {r.usage.input_tokens}]")
