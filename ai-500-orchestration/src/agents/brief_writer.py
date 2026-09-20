"""Brief Writer specialist agent.

Renders the final advisor-facing "morning brief" once compliance approves.
Deliberately writes ONLY the brief text — no meta-commentary — so downstream
consumers can hand it straight to the advisor's inbox.
"""
from __future__ import annotations

BRIEF_WRITER_INSTRUCTIONS = """You are the Brief Writer for Ridgevault Financial.
Given the analyst read + risk summary + compliance approval, produce the final
"morning brief" the advisor will read. Format:
- One-sentence executive summary.
- Bulleted list of the three most important items (movers, risk, watch).
- Closing disclosure sentence exactly as: "Not investment advice; consult your relationship manager."
Output ONLY the brief text — no preamble, no meta-commentary. Under 180 words."""


def build_agent(project, model: str):
    from agent_framework.azure import AzureAIAgentClient
    from agent_framework import ChatAgent

    client = AzureAIAgentClient(project_client=project, model=model)
    return ChatAgent(
        name="brief_writer",
        instructions=BRIEF_WRITER_INSTRUCTIONS,
        chat_client=client,
    )
