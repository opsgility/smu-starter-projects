"""Portfolio Analyst specialist agent.

Reads the portfolio and calls out overnight moves, concentration risk, and any
holdings the advisor should proactively discuss with the client. This is a
minimal specialist — one instruction, no external tools — so the lesson focuses
on ORCHESTRATION, not specialist depth.
"""
from __future__ import annotations

PORTFOLIO_ANALYST_INSTRUCTIONS = """You are the Portfolio Analyst for Ridgevault Financial.
Given a JSON portfolio and the previous day's close prices, produce a 3-4 bullet
morning read covering:
- Overnight movers of note (>= 1.5% absolute move).
- Concentration risks (any single holding > 20% of portfolio value).
- Any holding the advisor should proactively discuss.
Keep it under 120 words. No hedging language."""


def build_agent(project, model: str):
    """Return an Agent Framework ChatAgent for the Portfolio Analyst role.

    Kept as a factory so the sequential + graph orchestrators can both reuse it.
    """
    from agent_framework.azure import AzureAIAgentClient
    from agent_framework import ChatAgent

    client = AzureAIAgentClient(project_client=project, model=model)
    return ChatAgent(
        name="portfolio_analyst",
        instructions=PORTFOLIO_ANALYST_INSTRUCTIONS,
        chat_client=client,
    )
