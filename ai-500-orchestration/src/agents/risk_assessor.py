"""Risk Assessor specialist agent.

Consumes the analyst's read and produces a stress-test summary. Minimal
specialist by design.
"""
from __future__ import annotations

RISK_ASSESSOR_INSTRUCTIONS = """You are the Risk Assessor for Ridgevault Financial.
Given the Portfolio Analyst's morning read plus the raw portfolio JSON, produce
a 3-bullet risk summary covering:
- Drawdown exposure under a -5% equity shock.
- Sector concentration risk (any sector > 30% of portfolio value).
- One "watch item" the advisor should monitor today.
Keep it under 100 words. Use concrete percentages, not vague language."""


def build_agent(project, model: str):
    from agent_framework.azure import AzureAIAgentClient
    from agent_framework import ChatAgent

    client = AzureAIAgentClient(project_client=project, model=model)
    return ChatAgent(
        name="risk_assessor",
        instructions=RISK_ASSESSOR_INSTRUCTIONS,
        chat_client=client,
    )
