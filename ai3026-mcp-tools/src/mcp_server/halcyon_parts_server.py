"""Halcyon spare-parts + repair-cost MCP server.

Exposes two tools via fastmcp:
  - lookup_part(part_number)      — returns the parts record from data/parts.json
  - estimate_repair_cost(claim_id) — returns a labor + parts estimate for a claim

Both are consumed by the Foundry agent in ../mcp_client/halcyon_repair_agent.py.

Run: python src/mcp_server/halcyon_parts_server.py
"""
from __future__ import annotations
import json
from pathlib import Path

from fastmcp import FastMCP


DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "parts.json"

with DATA_FILE.open() as fh:
    _parts = json.load(fh)
PARTS_BY_NUMBER: dict[str, dict] = {p["part_number"]: p for p in _parts}


# Fictional Halcyon claim → repair-cost dict. In production this would be a
# Halcyon Repair Estimator API; here we hard-code five scenarios so the lesson
# has deterministic behavior.
CLAIM_COST_TABLE: dict[str, dict] = {
    "CLM-2026-091501": {"parts_cost": 1240.50, "labor_hours": 6.5, "labor_rate": 145.00, "total": 2183.00},
    "CLM-2026-091502": {"parts_cost": 3480.00, "labor_hours": 14.0, "labor_rate": 145.00, "total": 5510.00},
    "CLM-2026-091503": {"parts_cost": 620.00, "labor_hours": 3.0, "labor_rate": 145.00, "total": 1055.00},
    "CLM-2026-091504": {"parts_cost": 8900.00, "labor_hours": 32.0, "labor_rate": 165.00, "total": 14180.00},
    "CLM-2026-091505": {"parts_cost": 210.00, "labor_hours": 1.0, "labor_rate": 125.00, "total": 335.00},
}


mcp = FastMCP("halcyon-parts")


@mcp.tool()
def lookup_part(part_number: str) -> dict:
    """Look up a Halcyon-approved spare part by manufacturer part number.

    Args:
        part_number: The manufacturer part number, e.g. "47B-991".

    Returns:
        Part record with description, unit_price, weight_kg, category, supplier.
        Returns {"error": "..."} when the part is not in Halcyon's approved catalog.
    """
    record = PARTS_BY_NUMBER.get(part_number)
    if record is None:
        return {"error": f"Part {part_number!r} not in Halcyon's approved catalog"}
    return record


@mcp.tool()
def estimate_repair_cost(claim_id: str) -> dict:
    """Estimate parts + labor cost for a Halcyon claim.

    Args:
        claim_id: The Halcyon claim ID, e.g. "CLM-2026-091501".

    Returns:
        Cost estimate with parts_cost, labor_hours, labor_rate, and total.
        Returns {"error": "..."} for unknown claim IDs.
    """
    record = CLAIM_COST_TABLE.get(claim_id)
    if record is None:
        return {"error": f"No repair estimate on file for {claim_id!r}"}
    return record


if __name__ == "__main__":
    # Bind to localhost, port 8123. Change via MCP_SERVER_URL env var and update
    # the client's server_url to match.
    mcp.run(transport="http", host="127.0.0.1", port=8123)
