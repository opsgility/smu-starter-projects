"""Compliance Officer specialist agent.

Checks the analyst + risk output against Ridgevault's restricted list and
required disclosures. Emits an explicit "APPROVE" or "REJECT: <reason>" verdict
on its final line so the orchestrators can branch on it cheaply.
"""
from __future__ import annotations

COMPLIANCE_OFFICER_INSTRUCTIONS = """You are the Compliance Officer for Ridgevault Financial.

Ridgevault's restricted list for this session: ["ACME.Q", "PONZI.Q"].
Every morning brief must:
- Disclose any holding of a restricted-list ticker to the advisor.
- Include the boilerplate "Not investment advice; consult your relationship manager."
- Avoid forward-looking language ("will", "guaranteed", "certain").

Given the analyst read + risk summary, review for violations.
Reply in this exact shape:
Line 1: Two-sentence review commentary.
Line 2: One of exactly these two literal strings, no other text on the line:
  APPROVE
  REJECT: <one-line reason>
"""


def build_agent(project, model: str):
    from agent_framework.azure import AzureAIAgentClient
    from agent_framework import ChatAgent

    client = AzureAIAgentClient(project_client=project, model=model)
    return ChatAgent(
        name="compliance_officer",
        instructions=COMPLIANCE_OFFICER_INSTRUCTIONS,
        chat_client=client,
    )
