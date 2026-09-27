"""COMPLETE: 4 production tools + schemas."""

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
CUSTOMERS = json.loads((DATA / "customers.json").read_text(encoding="utf-8"))
TICKETS = json.loads((DATA / "tickets.json").read_text(encoding="utf-8"))
AUDIT_LOG: list[dict] = []


def get_customer_status(customer_id: str) -> str:
    c = CUSTOMERS.get(customer_id)
    if c is None:
        return json.dumps({"error": f"customer_id '{customer_id}' not found"})
    return json.dumps(c)


def search_recent_tickets(customer_id: str, limit: int = 3) -> str:
    if customer_id not in CUSTOMERS:
        return json.dumps({"error": f"customer_id '{customer_id}' not found"})
    tickets = TICKETS.get(customer_id, [])
    return json.dumps({"tickets": tickets[:limit]})


def apply_refund(customer_id: str, amount_usd: float, reason: str) -> str:
    if customer_id not in CUSTOMERS:
        return json.dumps({"status": "failed", "error": f"customer '{customer_id}' not found"})
    c = CUSTOMERS[customer_id]
    if c["status"] != "active":
        return json.dumps({"status": "failed", "error": f"cannot refund status={c['status']}"})
    action = {"tool": "apply_refund", "customer_id": customer_id, "amount_usd": amount_usd, "reason": reason, "status": "ok"}
    AUDIT_LOG.append(action)
    return json.dumps(action)


def escalate_to_human(customer_id: str, reason: str, priority: str = "medium") -> str:
    if customer_id not in CUSTOMERS:
        return json.dumps({"status": "failed", "error": f"customer '{customer_id}' not found"})
    csm = CUSTOMERS[customer_id].get("csm") or "unassigned-queue"
    action = {"tool": "escalate_to_human", "customer_id": customer_id, "reason": reason, "priority": priority, "routed_to": csm, "status": "ok"}
    AUDIT_LOG.append(action)
    return json.dumps(action)


TOOL_SCHEMAS = [
    {"name": "get_customer_status",
     "description": "Look up customer tier, status, CSM by customer_id. Call FIRST for any customer request.",
     "input_schema": {"type": "object", "properties": {"customer_id": {"type": "string"}}, "required": ["customer_id"]}},
    {"name": "search_recent_tickets",
     "description": "Fetch recent tickets for Pro/Enterprise customers to understand patterns.",
     "input_schema": {"type": "object", "properties": {"customer_id": {"type": "string"}, "limit": {"type": "integer", "default": 3}}, "required": ["customer_id"]}},
    {"name": "apply_refund",
     "description": "SIDE-EFFECT: process refund. Only on active accounts. Fails on suspended/cancelled.",
     "input_schema": {"type": "object", "properties": {"customer_id": {"type": "string"}, "amount_usd": {"type": "number"}, "reason": {"type": "string"}}, "required": ["customer_id", "amount_usd", "reason"]}},
    {"name": "escalate_to_human",
     "description": "SIDE-EFFECT: route ticket to human. Use for suspended/cancelled accounts, compliance, judgment calls.",
     "input_schema": {"type": "object", "properties": {"customer_id": {"type": "string"}, "reason": {"type": "string"}, "priority": {"type": "string", "enum": ["low", "medium", "high"]}}, "required": ["customer_id", "reason"]}},
]

TOOL_IMPLS = {"get_customer_status": get_customer_status, "search_recent_tickets": search_recent_tickets,
              "apply_refund": apply_refund, "escalate_to_human": escalate_to_human}
