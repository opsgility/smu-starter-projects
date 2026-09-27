"""4-tool schema + implementations for Orion's support-triage agent."""

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
CUSTOMERS = json.loads((DATA / "customers.json").read_text(encoding="utf-8"))
TICKETS = json.loads((DATA / "tickets.json").read_text(encoding="utf-8"))

# In-memory audit log of side-effect tools (refund, escalate) so tests can assert what happened.
AUDIT_LOG: list[dict] = []


def get_customer_status(customer_id: str) -> str:
    """Read-only lookup."""
    c = CUSTOMERS.get(customer_id)
    if c is None:
        return json.dumps({"error": f"customer_id '{customer_id}' not found"})
    return json.dumps(c)


def search_recent_tickets(customer_id: str, limit: int = 3) -> str:
    """Read-only lookup."""
    if customer_id not in CUSTOMERS:
        return json.dumps({"error": f"customer_id '{customer_id}' not found"})
    tickets = TICKETS.get(customer_id, [])
    return json.dumps({"tickets": tickets[:limit], "total_returned": min(len(tickets), limit)})


def apply_refund(customer_id: str, amount_usd: float, reason: str) -> str:
    """Side-effect tool — logs a refund action."""
    if customer_id not in CUSTOMERS:
        return json.dumps({"status": "failed", "error": f"customer_id '{customer_id}' not found"})
    c = CUSTOMERS[customer_id]
    if c["status"] != "active":
        return json.dumps({"status": "failed",
                           "error": f"cannot process refund for account with status={c['status']}"})
    action = {"tool": "apply_refund", "customer_id": customer_id,
              "amount_usd": amount_usd, "reason": reason, "status": "ok"}
    AUDIT_LOG.append(action)
    return json.dumps(action)


def escalate_to_human(customer_id: str, reason: str, priority: str = "medium") -> str:
    """Side-effect tool — logs an escalation."""
    if customer_id not in CUSTOMERS:
        return json.dumps({"status": "failed", "error": f"customer_id '{customer_id}' not found"})
    csm = CUSTOMERS[customer_id].get("csm") or "unassigned-queue"
    action = {"tool": "escalate_to_human", "customer_id": customer_id, "reason": reason,
              "priority": priority, "routed_to": csm, "status": "ok"}
    AUDIT_LOG.append(action)
    return json.dumps(action)


TOOL_SCHEMAS = [
    {
        "name": "get_customer_status",
        "description": ("Look up a customer's subscription tier, open incident count, account status "
                       "(active/suspended/cancelled), and assigned Customer Success Manager. "
                       "Call this FIRST for any customer-specific request before deciding actions."),
        "input_schema": {"type": "object",
                         "properties": {"customer_id": {"type": "string"}},
                         "required": ["customer_id"]},
    },
    {
        "name": "search_recent_tickets",
        "description": ("Fetch a customer's most recent support tickets. Use this to see a pattern "
                       "(recurring outages? single ticket?) before recommending goodwill credits or "
                       "escalations. Only call this for Pro or Enterprise customers — Starter "
                       "customers don't warrant ticket-history review."),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
                "limit": {"type": "integer", "default": 3, "description": "Max tickets to return."},
            },
            "required": ["customer_id"],
        },
    },
    {
        "name": "apply_refund",
        "description": ("SIDE-EFFECT tool: process a refund on the customer's account. Only call this "
                       "AFTER confirming the account is active AND the situation warrants a refund. "
                       "Cannot process refunds against suspended or cancelled accounts."),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
                "amount_usd": {"type": "number", "description": "Refund amount in USD."},
                "reason": {"type": "string", "description": "Short reason string for the audit log."},
            },
            "required": ["customer_id", "amount_usd", "reason"],
        },
    },
    {
        "name": "escalate_to_human",
        "description": ("SIDE-EFFECT tool: route the ticket to a human. Use when: (a) the customer's "
                       "situation requires judgment beyond the agent's authority, (b) the account is "
                       "suspended or cancelled and the customer needs manual assistance, or (c) the "
                       "customer explicitly asked for a human."),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_id": {"type": "string"},
                "reason": {"type": "string"},
                "priority": {"type": "string",
                             "enum": ["low", "medium", "high"],
                             "description": "Routing priority."},
            },
            "required": ["customer_id", "reason"],
        },
    },
]


TOOL_IMPLS = {
    "get_customer_status": get_customer_status,
    "search_recent_tickets": search_recent_tickets,
    "apply_refund": apply_refund,
    "escalate_to_human": escalate_to_human,
}
