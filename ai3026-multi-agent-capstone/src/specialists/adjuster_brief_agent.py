"""Halcyon adjuster-brief agent — local Microsoft Agent Framework agent.

Given the outputs of coverage_agent and damage_assessment_server, drafts the adjuster's
first-touch brief that goes into Halcyon Assist.
"""
from __future__ import annotations
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential


ADJUSTER_BRIEF_INSTRUCTIONS = """\
You are the Halcyon adjuster-brief writer. Given:

  - The original claim payload
  - The coverage verification JSON (from HalcyonCoverageAgent)
  - The damage assessment JSON (from HalcyonDamageAssessment via A2A)

Draft the adjuster's first-touch brief — 3 to 5 short paragraphs — covering:

  1. What happened (one paragraph, plain language).
  2. Coverage verdict + policy lines that respond.
  3. Damage severity + preliminary cost band.
  4. What the adjuster should do next (call the policyholder, order photos,
     schedule a body-shop inspection, escalate to a senior adjuster, etc.).
  5. Anything the two upstream agents flagged for follow-up.

Keep it factual and short. This lands in Halcyon Assist as the first entry an adjuster
sees when they open a claim.
"""


def build_adjuster_brief_agent() -> Agent:
    """Construct the adjuster_brief_agent. Called by orchestrator.py."""
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model = os.environ["FOUNDRY_MODEL"]
    client = FoundryChatClient(
        project_endpoint=endpoint,
        model_deployment_name=model,
        credential=DefaultAzureCredential(),
    )
    return Agent(
        chat_client=client,
        name="HalcyonAdjusterBriefAgent",
        instructions=ADJUSTER_BRIEF_INSTRUCTIONS,
    )
