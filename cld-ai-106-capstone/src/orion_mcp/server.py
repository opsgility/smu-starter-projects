"""Complete Orion MCP server: 3 tools + 2 resources + 1 prompt."""

import json
from typing import Literal

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("orion")


CUSTOMERS = {
    "acme-corp":  {"tier": "Enterprise", "status": "active"},
    "widget-inc": {"tier": "Starter",    "status": "suspended"},
    "beta-labs":  {"tier": "Pro",        "status": "active"},
}
RUNBOOKS = {
    "sla": "Sev-1: 15min/4h. Sev-2: 1h/24h. Sev-3: 4h/72h.",
    "refund": "Refunds only on active accounts. Suspended → escalate.",
}
AUDIT: list[dict] = []


@mcp.tool()
def lookup_customer(customer_id: str) -> str:
    """Look up an Orion customer by id."""
    return json.dumps(CUSTOMERS.get(customer_id, {"error": "not found"}))


@mcp.tool()
def apply_refund(customer_id: str, amount_usd: float, reason: str) -> str:
    """Process a refund. Only works on active accounts."""
    c = CUSTOMERS.get(customer_id)
    if not c:
        return json.dumps({"status": "failed", "error": "not found"})
    if c["status"] != "active":
        return json.dumps({"status": "failed", "error": f"status={c['status']}"})
    action = {"tool": "apply_refund", "customer_id": customer_id, "amount_usd": amount_usd, "reason": reason}
    AUDIT.append(action)
    return json.dumps({"status": "ok", **action})


@mcp.tool()
def escalate_to_csm(customer_id: str, reason: str, priority: Literal["low","medium","high"] = "medium") -> str:
    """Escalate a ticket to the customer success manager."""
    action = {"tool": "escalate", "customer_id": customer_id, "reason": reason, "priority": priority}
    AUDIT.append(action)
    return json.dumps({"status": "ok", **action})


@mcp.resource("orion://runbook/{name}", mime_type="text/plain")
def runbook(name: str) -> str:
    """Fetch a runbook section by name."""
    return RUNBOOKS.get(name, f"(no runbook: {name})")


@mcp.resource("orion://config/current")
def config() -> str:
    """Current environment config."""
    return json.dumps({"env": "prod", "region": "us-east-1", "version": "2026.9.1"})


@mcp.prompt()
def review_ticket(ticket_text: str) -> str:
    """Review an Orion support ticket and recommend an action."""
    return (f"Review this Orion Analytics ticket and recommend an action. Consider "
            f"customer status, refund policy, and escalation rules.\n\n{ticket_text}")
