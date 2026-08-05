# RAG client placeholder. Lesson 6 fills in the AI Search tool wiring so
# Halcyon Assist can ground answers in the halcyon-policies index.
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value or value.startswith("<"):
        print(f"[rag_client] Missing env var: set this variable in .env -> {name}")
        sys.exit(1)
    return value


def build_rag_agent() -> Agent:
    """Return the Halcyon Assist agent with an AI Search grounding tool attached.

    Lesson 6 replaces the NotImplementedError below with the real wiring.
    """
    load_dotenv()

    endpoint = require_env("AZURE_AI_PROJECT_ENDPOINT")
    deployment = require_env("AZURE_AI_CHAT_DEPLOYMENT")
    search_endpoint = require_env("AZURE_AI_SEARCH_ENDPOINT")
    search_index = require_env("AZURE_AI_SEARCH_INDEX")

    client = FoundryChatClient(
        project_endpoint=endpoint,
        model=deployment,
        credential=DefaultAzureCredential(),
    )

    # --- ai_search tool wiring ---
    # TODO Lesson 6 Exercise 2: resolve the Foundry project connection ID for
    # the AI Search resource (AZURE_AI_SEARCH_ENDPOINT) and attach it as the
    # first tool on this agent using FoundryChatClient.get_ai_search_tool(...).
    # TODO Lesson 6 Exercise 3: extend the SYSTEM_PROMPT in copilot_agent.py so
    # the agent always cites the policy document ID it grounded on.
    raise NotImplementedError(
        "Lesson 6: attach the AI Search grounding tool for index "
        f"{search_index!r} at {search_endpoint!r}, then return the Agent."
    )
