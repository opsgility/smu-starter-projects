"""Typed tools with Literal enums + Pydantic models + validators."""

from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("orion-typed")


# TODO 1: set_priority tool with Literal enum for priority.
# HINT:
#   @mcp.tool()
#   def set_priority(ticket_id: str, priority: Literal["low","medium","high"]) -> dict:
#       """Set the priority of a ticket."""
#       return {"ticket_id": ticket_id, "priority": priority, "status": "ok"}


class RefundRequest(BaseModel):
    customer_id: str
    amount_usd: float = Field(gt=0, le=10000, description="Refund amount, max 10k")
    reason: str = Field(min_length=10)


# TODO 2: process_refund tool using RefundRequest Pydantic model.
# HINT:
#   @mcp.tool()
#   def process_refund(req: RefundRequest) -> dict:
#       """Process a customer refund."""
#       return {"status": "ok", "customer_id": req.customer_id, "amount": req.amount_usd}


class SLARule(BaseModel):
    severity: Literal[1, 2, 3]
    response_min: int = Field(gt=0)

    @field_validator("response_min")
    @classmethod
    def enforce_bounds(cls, v, info):
        limits = {1: 15, 2: 60, 3: 240}
        sev = info.data.get("severity")
        if sev and v > limits[sev]:
            raise ValueError(f"Sev-{sev} response cannot exceed {limits[sev]} min")
        return v


# TODO 3: register_sla_rule tool using SLARule model with the cross-field validator.
# HINT:
#   @mcp.tool()
#   def register_sla_rule(rule: SLARule) -> dict:
#       """Register an SLA rule; enforces per-severity response caps."""
#       return {"status": "ok", "sev": rule.severity, "response_min": rule.response_min}


if __name__ == "__main__":
    mcp.run()
