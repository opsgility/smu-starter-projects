"""Orion invoice-processing pipeline.
Vision router → Haiku classifier → Sonnet extractor → validator."""

import base64, json, sys, os
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()


ROUTER_TOOLS = [
    {"name": "route_invoice", "description": "Multi-line-item bill with total + due date",
     "input_schema": {"type": "object", "properties": {
         "vendor": {"type": "string"}, "total": {"type": "number"},
         "line_items": {"type": "array", "items": {"type": "object"}},
         "due_date": {"type": "string"}
     }}},
    {"name": "route_receipt", "description": "Point-of-sale purchase receipt",
     "input_schema": {"type": "object", "properties": {
         "merchant": {"type": "string"}, "total": {"type": "number"}
     }}},
    {"name": "route_unknown", "description": "Not recognizable",
     "input_schema": {"type": "object", "properties": {
         "reason": {"type": "string"}
     }}},
]


def load_doc(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    if path.endswith(".pdf"):
        return {"type": "document", "source": {"type": "base64",
                                                "media_type": "application/pdf", "data": data}}
    m = "image/png" if path.endswith(".png") else "image/jpeg"
    return {"type": "image", "source": {"type": "base64", "media_type": m, "data": data}}


def process(doc_path):
    block = load_doc(doc_path)
    r = client.messages.create(
        model="claude-sonnet-5", max_tokens=2048,
        tools=ROUTER_TOOLS,
        messages=[{"role": "user", "content": [
            block,
            {"type": "text", "text": "Classify + extract this document."}]}]
    )
    tool_call = next((b for b in r.content if b.type == "tool_use"), None)
    if not tool_call:
        return {"routed": "no_tool", "raw": [b.type for b in r.content]}
    return {"routed": tool_call.name, "data": tool_call.input,
            "cost_usd": round(r.usage.input_tokens * 3/1e6 + r.usage.output_tokens * 15/1e6, 6)}


def validate(result):
    if result["routed"] == "route_invoice":
        total = result["data"].get("total")
        items = result["data"].get("line_items", [])
        item_sum = sum(i.get("amount", 0) for i in items)
        return {"ok": abs(total - item_sum) < 1.0, "total": total, "item_sum": item_sum} \
               if total else {"ok": False, "reason": "no total"}
    return {"ok": True, "note": "no validation for this route"}


def main():
    paths = sys.argv[1:] or ["invoice.pdf"]
    for p in paths:
        print(f"\n=== {p} ===")
        r = process(p)
        print(json.dumps(r, indent=2))
        print("validation:", json.dumps(validate(r)))


if __name__ == "__main__":
    main()
