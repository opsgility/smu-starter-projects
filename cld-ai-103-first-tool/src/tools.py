"""Tool definitions + implementations — COMPLETE, do not edit.

Contains:
  - TOOL_SCHEMAS: the list of tool schemas you pass to client.messages.create(tools=...)
  - TOOL_IMPLS: dict mapping tool_name -> Python callable

The agent loop in agent.py imports both and dispatches Claude's tool_use
requests to the right function.
"""

import json
from pathlib import Path


CUSTOMERS_PATH = Path(__file__).resolve().parent.parent / "data" / "customers.json"
CUSTOMERS = json.loads(CUSTOMERS_PATH.read_text(encoding="utf-8"))


TOOL_SCHEMAS = [
    {
        "name": "get_customer_status",
        "description": (
            "Look up a customer's current subscription tier, open incident count, "
            "account status (active/suspended/cancelled), and next renewal date. "
            "Use this when a support ticket mentions a customer_id and you need "
            "their current account state before deciding an action."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "The customer's identifier (e.g. 'acme-corp')",
                },
            },
            "required": ["customer_id"],
        },
    }
]


def get_customer_status(customer_id: str) -> str:
    """Return the customer's status as a JSON string (or an error dict)."""
    customer = CUSTOMERS.get(customer_id)
    if customer is None:
        return json.dumps({"error": f"customer_id '{customer_id}' not found"})
    return json.dumps(customer)


TOOL_IMPLS = {
    "get_customer_status": get_customer_status,
}
