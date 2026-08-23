"""Halcyon damage-assessment agent — hosted as a REMOTE A2A server.

Runs as its own process. The orchestrator discovers it via the AgentCard endpoint
(GET http://127.0.0.1:8500/.well-known/agent.json) and calls it over A2A.

This models the real Halcyon architecture where damage_assessment is owned by a
different team and runs as its own service.

Run: python src/specialists/damage_assessment_server.py
"""
from __future__ import annotations
import os

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.types import AgentCard, AgentCapabilities, AgentSkill
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


DAMAGE_ASSESSMENT_INSTRUCTIONS = """\
You are the Halcyon damage-assessment agent. Given a claim payload with a damage_description
and optional photo_urls, estimate severity and cost band:

  1. severity: 'minor' / 'moderate' / 'major' / 'total_loss'
  2. cost_band: '$0-$1000' / '$1000-$5000' / '$5000-$15000' / '$15000-$50000' / '$50000+'
  3. rationale: one-sentence justification
  4. requires_shop_inspection: true / false
  5. estimated_days_to_complete: integer

Output ONLY JSON with those keys — no prose wrapper.
"""


def build_damage_agent() -> Agent:
    """Construct the damage assessment agent."""
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model = os.environ["FOUNDRY_MODEL"]
    client = FoundryChatClient(
        project_endpoint=endpoint,
        model_deployment_name=model,
        credential=DefaultAzureCredential(),
    )
    return Agent(
        chat_client=client,
        name="HalcyonDamageAssessment",
        instructions=DAMAGE_ASSESSMENT_INSTRUCTIONS,
    )


def build_agent_card() -> AgentCard:
    """The AgentCard the A2A client fetches via /.well-known/agent.json."""
    return AgentCard(
        name="HalcyonDamageAssessment",
        description="Halcyon Insurance damage-assessment specialist agent — hosted service, consumed by the claims-triage orchestrator via A2A.",
        url=os.environ.get("DAMAGE_A2A_URL", "http://127.0.0.1:8500"),
        version="1.0.0",
        capabilities=AgentCapabilities(streaming=False, pushNotifications=False),
        skills=[
            AgentSkill(
                id="assess_damage",
                name="Assess damage severity and cost band",
                description="Given a claim payload with damage_description, returns severity, cost_band, rationale, and inspection recommendation.",
                tags=["insurance", "claims", "damage-assessment"],
            )
        ],
        defaultInputModes=["application/json", "text/plain"],
        defaultOutputModes=["application/json"],
    )


def main() -> None:
    load_dotenv()
    # TODO (Ex 3): wire the Agent Framework `Agent` (build_damage_agent()) as the
    # request-handler backing this A2A app. The A2AStarletteApplication constructor
    # varies slightly across a2a-sdk releases — check the lab agent's cheat sheet for
    # the current shape (typically a RequestHandler wrapping the Agent + AgentCard).
    agent_card = build_agent_card()
    app: A2AStarletteApplication = ...  # type: ignore[assignment]

    # Bind to 127.0.0.1:8500 — matches DAMAGE_A2A_URL default in .env.example.
    uvicorn.run(app.build(), host="127.0.0.1", port=8500)


if __name__ == "__main__":
    main()
