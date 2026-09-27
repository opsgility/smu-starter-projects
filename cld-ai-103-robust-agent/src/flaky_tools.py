"""4 tools with configurable failure injection for stress-testing the agent."""

import json
import os
import random
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
CUSTOMERS = json.loads((DATA / "customers.json").read_text(encoding="utf-8"))


class TransientToolError(Exception):
    """Simulated transient failure (429 / 503 / timeout equivalent). Should be retried."""
    status_code = 429


class PermanentToolError(Exception):
    """Simulated permanent failure (400 bad request). Should NOT be retried."""
    status_code = 400


# Failure injection controls — read from env so tests can flip them.
def _flaky_prob() -> float:
    """Probability that a tool call raises TransientToolError. Default 0.4 (40%)."""
    return float(os.environ.get("FLAKY_PROB", "0.4"))


def _permanent_tool() -> str:
    """Name of a tool that always raises PermanentToolError (empty = no permanent failure)."""
    return os.environ.get("PERMANENT_FAIL_TOOL", "")


CALL_LOG: list[dict] = []


def _maybe_fail(tool_name: str):
    CALL_LOG.append({"tool": tool_name, "when": len(CALL_LOG) + 1})
    if tool_name == _permanent_tool():
        raise PermanentToolError(f"tool {tool_name} configured to always fail permanently (400)")
    if random.random() < _flaky_prob():
        raise TransientToolError(f"tool {tool_name} hit simulated 429 rate limit")


def get_customer_status(customer_id: str) -> str:
    _maybe_fail("get_customer_status")
    c = CUSTOMERS.get(customer_id)
    if c is None:
        return json.dumps({"error": f"customer_id '{customer_id}' not found"})
    return json.dumps(c)


def search_recent_tickets(customer_id: str, limit: int = 3) -> str:
    _maybe_fail("search_recent_tickets")
    if customer_id not in CUSTOMERS:
        return json.dumps({"error": f"customer_id '{customer_id}' not found"})
    return json.dumps({"tickets": [{"id": f"T-{i}", "summary": "example"} for i in range(min(limit, 3))]})


def apply_refund(customer_id: str, amount_usd: float, reason: str) -> str:
    _maybe_fail("apply_refund")
    if customer_id not in CUSTOMERS:
        return json.dumps({"status": "failed", "error": f"customer_id '{customer_id}' not found"})
    c = CUSTOMERS[customer_id]
    if c["status"] != "active":
        return json.dumps({"status": "failed", "error": f"cannot refund status={c['status']}"})
    return json.dumps({"status": "ok", "customer_id": customer_id, "amount_usd": amount_usd})


def escalate_to_human(customer_id: str, reason: str, priority: str = "medium") -> str:
    _maybe_fail("escalate_to_human")
    return json.dumps({"status": "ok", "customer_id": customer_id, "routed_to": "on-call-queue"})


TOOL_SCHEMAS = [
    {"name": "get_customer_status",
     "description": "Look up a customer's tier and status by customer_id.",
     "input_schema": {"type": "object",
                      "properties": {"customer_id": {"type": "string"}},
                      "required": ["customer_id"]}},
    {"name": "search_recent_tickets",
     "description": "Fetch a customer's recent tickets. Only for Pro or Enterprise tier.",
     "input_schema": {"type": "object",
                      "properties": {"customer_id": {"type": "string"},
                                     "limit": {"type": "integer", "default": 3}},
                      "required": ["customer_id"]}},
    {"name": "apply_refund",
     "description": "Process a refund. Requires active account.",
     "input_schema": {"type": "object",
                      "properties": {"customer_id": {"type": "string"},
                                     "amount_usd": {"type": "number"},
                                     "reason": {"type": "string"}},
                      "required": ["customer_id", "amount_usd", "reason"]}},
    {"name": "escalate_to_human",
     "description": "Route ticket to a human when situation exceeds agent authority.",
     "input_schema": {"type": "object",
                      "properties": {"customer_id": {"type": "string"},
                                     "reason": {"type": "string"},
                                     "priority": {"type": "string", "enum": ["low", "medium", "high"]}},
                      "required": ["customer_id", "reason"]}},
]

TOOL_IMPLS = {
    "get_customer_status": get_customer_status,
    "search_recent_tickets": search_recent_tickets,
    "apply_refund": apply_refund,
    "escalate_to_human": escalate_to_human,
}
