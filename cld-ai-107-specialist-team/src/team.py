"""Router + 3 specialist agents."""

import json, os, sys
from dotenv import load_dotenv
import anthropic


ROUTE_SCHEMA = {
    "name": "route_request",
    "input_schema": {
        "type": "object",
        "properties": {"specialist": {"type": "string", "enum": ["billing", "technical", "feature_request", "other"]}},
        "required": ["specialist"],
    },
}


def route(client, model, request: str) -> str:
    prompt = f"Classify which specialist handles this request:\n{request}\nUse route_request."
    resp = client.messages.create(model=model, max_tokens=100,
        tools=[ROUTE_SCHEMA], tool_choice={"type":"tool","name":"route_request"},
        messages=[{"role":"user","content":prompt}])
    return next(b.input for b in resp.content if b.type == "tool_use")["specialist"]


SPECIALISTS = {
    "billing": {
        "system": "You handle billing. Tools: process_refund, check_invoice. Refuse non-billing questions.",
        "tools": [
            {"name":"process_refund","description":"Process refund.","input_schema":{"type":"object","properties":{"amount":{"type":"number"}},"required":["amount"]}},
            {"name":"check_invoice","description":"Check invoice.","input_schema":{"type":"object","properties":{"month":{"type":"string"}},"required":["month"]}},
        ],
    },
    "technical": {
        "system": "You handle technical issues. Tools: check_api_status, restart_service. Refuse non-technical questions.",
        "tools": [
            {"name":"check_api_status","description":"Check API health.","input_schema":{"type":"object","properties":{"endpoint":{"type":"string"}},"required":["endpoint"]}},
            {"name":"restart_service","description":"Restart a service.","input_schema":{"type":"object","properties":{"service":{"type":"string"}},"required":["service"]}},
        ],
    },
    "feature_request": {
        "system": "You handle feature requests. Tools: log_feature. Refuse non-feature questions.",
        "tools": [
            {"name":"log_feature","description":"Log a feature request.","input_schema":{"type":"object","properties":{"feature":{"type":"string"}},"required":["feature"]}},
        ],
    },
    "other": {"system": "You handle miscellaneous. No tools.", "tools": []},
}


def specialist_handle(client, model, specialist_name: str, request: str) -> str:
    spec = SPECIALISTS[specialist_name]
    # Simple 1-turn handling (in production would loop like L2)
    resp = client.messages.create(model=model, max_tokens=500,
        system=spec["system"],
        tools=spec["tools"] if spec["tools"] else [],
        messages=[{"role":"user","content":request}])
    parts = []
    for b in resp.content:
        if b.type == "text": parts.append(b.text)
        elif b.type == "tool_use": parts.append(f"[calling tool {b.name}({b.input})]")
    return " ".join(parts) if parts else "(no response)"


def handle_request(client, model, request: str) -> dict:
    """TODO: route the request, then hand off to that specialist. Return {'routed_to', 'answer'}.
    HINT:
      specialist = route(client, model, request)
      answer = specialist_handle(client, model, specialist, request)
      return {"routed_to": specialist, "answer": answer}
    """
    raise NotImplementedError("TODO: implement handle_request")


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    requests = [
        "I need a $50 refund for last week's outage.",
        "Our /v2/analytics endpoint is returning 502s. Please investigate.",
        "Please add row-level permissions in the Compliance workspace.",
        "Just saying hi, love the product!",
    ]
    for r in requests:
        print(f"\n>>> {r}")
        try:
            result = handle_request(client, model, r)
        except NotImplementedError as e:
            print(f"TODO not filled: {e}"); return 1
        print(f"[routed → {result['routed_to']}]")
        print(f"  {result['answer'][:200]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
