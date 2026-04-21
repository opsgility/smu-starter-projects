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
MODEL = os.environ.get("MODEL_DEPLOYMENT", "gpt-4.1")
SEARCH_CONN = os.environ.get("AZURE_SEARCH_CONNECTION_ID", "")
SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX", "summitline-kb")

tracer = trace.get_tracer("summitline-capstone")


def _ship_status(order_id: str) -> dict:
    """Look up Summitline shipping status for an order.

    This is the custom :class:`FunctionTool` body the agent invokes when a
    user asks about orders. The lab ships with canned data — in production
    this would call the OMS.

    :param order_id: Order identifier like ``SUM-884210``.
    :return: dict with ``order_id``, ``status``, ``carrier``, ``eta_days``.
    """
    return {
        "order_id": order_id,
        "status": "in transit",
        "carrier": "FedEx",
        "eta_days": 3,
    }


def run(message: str) -> str:
    """Create a one-shot agent, process the message, tear the agent down.

    The agent is bound per-request so labs stay easy to reason about. The
    ``finally`` block calls :meth:`AgentsClient.delete_agent` so nothing
    leaks across invocations.
    """
    with tracer.start_as_current_span("summitline.agent.run") as span:
        span.set_attribute("message.chars", len(message))

        # TODO (Exercise 2 Step 2): instantiate AgentsClient(endpoint=PROJECT, credential=DefaultAzureCredential())
        # in a `with` block. Build a ToolSet that includes:
        #   - AzureAISearchTool(index_connection_id=SEARCH_CONN, index_name=SEARCH_INDEX,
        #                      query_type=AzureAISearchQueryType.SEMANTIC, top_k=5)
        #   - FunctionTool({_ship_status})
        # Call client.enable_auto_function_calls(toolset) BEFORE create_and_process.

        # TODO (Exercise 2 Step 2): call client.create_agent(model=MODEL,
        # name="summitline-concierge", instructions=<...>, tools=toolset.definitions,
        # tool_resources=toolset.resources). In a try/finally: threads.create,
        # messages.create(role="user"), runs.create_and_process(toolset=toolset),
        # then messages.list(order=ListSortOrder.ASCENDING) and return the
        # last assistant message's text. delete_agent in finally.
        raise NotImplementedError(
            "Complete TODOs in app/agent.py (Exercise 2 Step 2)."
        )
