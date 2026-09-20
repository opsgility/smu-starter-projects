"""Halcyon coverage-verification agent — local Microsoft Agent Framework agent.

Given a claim payload, verifies whether the policy in force covers the incident described.
Reads the policy's declared limits + riders from the claim payload (in production it would
call a policy admin service; here the payload embeds the policy so the capstone stays
self-contained).
"""
from __future__ import annotations
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential


COVERAGE_INSTRUCTIONS = """\
You are the Halcyon coverage-verification agent. Given a claim payload (JSON), decide:

  1. Is the incident described within the policy's coverage lines? (auto liability, property,
     umbrella, etc.)
  2. Does the incident type match a rider the policy has active? (water_damage, roadside, etc.)
  3. If coverage is uncertain, what specific policy language would the adjuster need to look up?

Output a JSON object with keys:
  - covered: true / false / uncertain
  - reason: one-sentence explanation
  - coverage_lines_used: list of policy limits that would apply
  - riders_used: list of active riders that apply
  - flags_for_adjuster: list of items the adjuster should confirm

Return ONLY the JSON — no prose wrapper.
"""


def build_coverage_agent() -> Agent:
    """Construct the coverage_agent. Called by orchestrator.py."""
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model = os.environ["FOUNDRY_MODEL"]
    client = FoundryChatClient(
        project_endpoint=endpoint,
        model_deployment_name=model,
        credential=DefaultAzureCredential(),
    )
    return Agent(
        chat_client=client,
        name="HalcyonCoverageAgent",
        instructions=COVERAGE_INSTRUCTIONS,
    )
