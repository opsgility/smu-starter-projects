"""/agent — AgentsClient 1.1.0 with AzureAISearchTool + FunctionTool (Exercise 2)."""

from __future__ import annotations

import os

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import (
    AzureAISearchQueryType,
    AzureAISearchTool,
    FunctionTool,
    ListSortOrder,
    ToolSet,
)
from azure.identity import DefaultAzureCredential
from opentelemetry import trace

PROJECT = os.environ.get("AZURE_AI_PROJECT_ENDPOINT", "")
MODEL = os.environ.get("MODEL_DEPLOYMENT", "gpt-5")
SEARCH_CONN = os.environ.get("AZURE_SEARCH_CONNECTION_ID", "")
SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX", "sib-osint-kb")

tracer = trace.get_tracer("sib-osint-capstone")


def _indicator_status(indicator_id: str) -> dict:
    """Look up SIB published threat-feed status for an OSINT indicator id.

    This is the custom :class:`FunctionTool` body the agent invokes when an
    analyst asks about an indicator. The lab ships with canned, non-classified
    data — in production this would call the bureau's published-feed service.

    :param indicator_id: Indicator identifier like ``OSINT-IND-2024-1042``.
    :return: dict with ``indicator_id``, ``status``, ``feed``, ``last_observed``.
    """
    return {
        "indicator_id": indicator_id,
        "status": "active",
        "feed": "SIB Public Indicator Feed v3",
        "last_observed": "2026-05-28",
    }


def run(message: str) -> str:
    """Create a one-shot agent, process the message, tear the agent down.

    The agent is bound per-request so labs stay easy to reason about. The
    ``finally`` block calls :meth:`AgentsClient.delete_agent` so nothing
    leaks across invocations.
    """
    with tracer.start_as_current_span("sib.agent.run") as span:
        span.set_attribute("message.chars", len(message))

        # Exercise 2 - Step 2 Start
        raise NotImplementedError("Complete Exercise 2 Step 2")
        # Exercise 2 - Step 2 End
