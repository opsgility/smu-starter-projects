"""Summitline Outfitters concierge — AgentsClient wiring and conversation driver.

Implemented across Exercises 1 and 2 of AI-103 Lesson 8:

- Exercise 1 Step 7 → TODOs 1 and 2 (ToolSet + create_agent)
- Exercise 2 Steps 1-3 → TODOs 3, 4, 5 (thread, messages + runs loop, transcript + cleanup)
"""
from __future__ import annotations

import os
from typing import List, Dict

from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FunctionTool, ToolSet, ListSortOrder

from app.functions import USER_FUNCTIONS


# Load PROJECT_ENDPOINT + MODEL_DEPLOYMENT_NAME from .env (sits next to test_client.py).
load_dotenv()

MODEL = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4.1-mini")

INSTRUCTIONS = (
    "You are the Summitline Outfitters concierge, a helpful assistant for a "
    "specialty outdoor-gear retailer. You help customer-support staff answer "
    "questions about shipping weather, bulk-order math, and stock levels for "
    "Summitline SKUs (pattern NW-SL-###). "
    "You have three tools: get_weather(city), calculate(expression), and "
    "lookup_inventory(sku). Use a tool whenever the user asks for weather, a "
    "numeric calculation, or product stock — never guess those values. "
    "When you answer, name the tool you used in one short sentence (for "
    "example, 'The get_weather tool reported 64 F and clear in Bend.'). "
    "Keep replies concise and friendly — one or two sentences."
)


def build_client() -> AgentsClient:
    """Construct an AgentsClient authenticated with DefaultAzureCredential.

    Reads ``PROJECT_ENDPOINT`` from the environment (loaded from ``.env`` at
    import time). No API keys are used — the signed-in az-cli principal must
    hold the ``Azure AI User`` role on the Foundry account.
    """
    endpoint = os.environ["PROJECT_ENDPOINT"]
    credential = DefaultAzureCredential()
    return AgentsClient(endpoint=endpoint, credential=credential)


def converse(messages: List[str]) -> List[Dict[str, str]]:
    """Run a single conversation through a fresh agent + thread.

    Each element of ``messages`` is sent as one user turn. The returned list
    is a chronological ``[{"role": ..., "text": ...}, ...]`` transcript of
    every text-bearing message on the thread (user and assistant).
    """
    with build_client() as client:
        # TODO 1 (Exercise 1 Step 7): Build a ToolSet and add a FunctionTool
        # that wraps USER_FUNCTIONS. Then call
        # client.enable_auto_function_calls(toolset) so the SDK dispatches
        # tool calls to your Python functions automatically.
        #
        # Example:
        #     toolset = ToolSet()
        #     toolset.add(FunctionTool(USER_FUNCTIONS))
        #     client.enable_auto_function_calls(toolset)

        # TODO 2 (Exercise 1 Step 7): Create the Summitline concierge agent
        # using client.create_agent(...). Pass model=MODEL,
        # name="summitline-concierge", instructions=INSTRUCTIONS,
        # tools=toolset.definitions, tool_resources=toolset.resources.

        # TODO 3 (Exercise 2 Step 1): Create a fresh thread for this
        # conversation with client.threads.create().

        # TODO 4 (Exercise 2 Step 2): For each user message in `messages`,
        # push it with client.messages.create(thread_id=..., role="user",
        # content=...) and then drive the turn with
        # client.runs.create_and_process(thread_id=..., agent_id=...). One
        # run per turn so each tool call completes before the next user
        # message arrives.

        # TODO 5 (Exercise 2 Step 3): List the thread messages in ascending
        # order with client.messages.list(thread_id=..., order=
        # ListSortOrder.ASCENDING), collapse each text-bearing message to
        # {"role": m.role, "text": m.text_messages[-1].text.value}, delete
        # the agent with client.delete_agent(agent.id), and return the
        # transcript.

        raise NotImplementedError(
            "Implement TODOs 1-5 in converse() — see Exercises 1 and 2."
        )
