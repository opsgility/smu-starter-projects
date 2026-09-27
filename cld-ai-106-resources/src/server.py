"""Resource-focused FastMCP server."""

import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("orion-resources")

CUSTOMERS = {
    "acme-corp":  {"tier": "Enterprise", "status": "active"},
    "widget-inc": {"tier": "Starter",    "status": "suspended"},
    "beta-labs":  {"tier": "Pro",        "status": "active"},
}

RUNBOOKS = {
    "sla":       "Sev-1: 15-min/4h. Sev-2: 1h/24h. Sev-3: 4h/72h.",
    "refund":    "Refunds only on active accounts.",
    "escalation":"Escalate suspended/cancelled accounts to CSM.",
}


# TODO 1: static resource orion://config/current returning JSON with env/region/version.
# HINT:
#   @mcp.resource("orion://config/current")
#   def config() -> str:
#       return json.dumps({"env":"prod","region":"us-east-1","version":"2026.9.1"})


# TODO 2: templated resource orion://customer/{customer_id}/profile.
# HINT:
#   @mcp.resource("orion://customer/{customer_id}/profile")
#   def customer_profile(customer_id: str) -> str:
#       c = CUSTOMERS.get(customer_id)
#       return json.dumps(c) if c else json.dumps({"error": f"unknown {customer_id}"})


# TODO 3: templated resource orion://runbook/{name} with mime_type="text/markdown".
# HINT:
#   @mcp.resource("orion://runbook/{name}", mime_type="text/markdown")
#   def runbook(name: str) -> str:
#       return RUNBOOKS.get(name, f"(no runbook named {name})")


if __name__ == "__main__":
    mcp.run()
