"""Prompts-focused FastMCP server."""

from typing import Literal
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("orion-prompts")


# TODO 1: prompt 'review-ticket' takes ticket_text, returns a review instruction.
# HINT:
#   @mcp.prompt()
#   def review_ticket(ticket_text: str) -> str:
#       """Review a support ticket and recommend an action."""
#       return f"Please review this support ticket:\n\n{ticket_text}\n\nRecommend a category and next step."


# TODO 2: prompt 'escalate-alert' with severity Literal + summary.
# HINT:
#   @mcp.prompt()
#   def escalate_alert(severity: Literal["low","medium","high"], summary: str) -> str:
#       """Draft an escalation email."""
#       return f"Draft an escalation email for a {severity} severity issue: {summary}"


# TODO 3: prompt 'weekly-digest' returning list of Message (multi-message).
# HINT:
#   from mcp.server.fastmcp.prompts import Message
#   @mcp.prompt()
#   def weekly_digest(week_of: str, incident_count: int) -> list:
#       """Draft a weekly incident digest."""
#       return [
#           Message(role="user", content=f"Week of {week_of}, we had {incident_count} incidents."),
#           Message(role="user", content="Draft a 3-paragraph digest for stakeholders."),
#       ]


if __name__ == "__main__":
    mcp.run()
