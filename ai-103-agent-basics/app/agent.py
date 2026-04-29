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
        # Exercise 1 - Step 7 Start
        raise NotImplementedError("Complete Exercise 1 Step 7, then continue with Exercise 2")
        # Exercise 1 - Step 7 End
