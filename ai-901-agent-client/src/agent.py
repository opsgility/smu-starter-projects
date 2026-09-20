"""Foundry single-agent starter — Microsoft Agent Framework.

Modern replacement for the retired `azure-ai-agents` SDK. Uses
`FoundryChatClient` + `Agent` from the Microsoft Agent Framework.

Refs (MS Learn):
- https://learn.microsoft.com/agent-framework/get-started/your-first-agent
- https://learn.microsoft.com/azure/foundry/agents/how-to/tools/function-calling
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from pydantic import Field

load_dotenv()

ENDPOINT = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
MODEL = os.environ.get("FOUNDRY_MODEL", "gpt-5-mini")


@tool(approval_mode="never_require")
def get_store_hours(
    store_id: Annotated[str, Field(description="Numeric store identifier, e.g. '42'.")],
) -> str:
    """Return the operating hours for a Northwind Horizon store — replace the hard-coded map in the exercise."""
    hours = {"42": "Mon–Sat 9–9, Sun 11–6", "17": "Mon–Fri 8–8, weekends closed"}
    return json.dumps({"store_id": store_id, "hours": hours.get(store_id, "unknown")})


def build_agent() -> Agent:
    if not ENDPOINT:
        raise RuntimeError("Set FOUNDRY_PROJECT_ENDPOINT in .env.")
    client = FoundryChatClient(
        project_endpoint=ENDPOINT,
        model=MODEL,
        credential=DefaultAzureCredential(),
    )
    return Agent(
        client=client,
        name="northwind-store-assistant",
        instructions=(
            "You are a helpful in-store assistant for Northwind Horizon. "
            "When asked about store hours, call the get_store_hours tool. "
            "Be concise."
        ),
        tools=[get_store_hours],
    )


async def create_agent() -> None:
    """Verify the agent configuration is loadable and reachable.

    Agent Framework agents are ephemeral in-process — there is no AGENT_ID to
    persist. The exercise walks you through building the agent + tools.
    """
    agent = build_agent()
    print(f"Agent ready: {agent.name} (model={MODEL})")
    print("Send a message with --chat 'your question'.")


async def chat_once(message: str) -> None:
    """TODO (exercise): send `message` through the agent and print the response.

    Hint (MS Learn — https://learn.microsoft.com/agent-framework/get-started/your-first-agent):

        agent = build_agent()
        result = await agent.run(message)
        print(result.text)

    Trace the tool-call lifecycle by inspecting `result.messages`.
    """
    raise NotImplementedError(
        "Exercise step: call `await agent.run(message)` and print the reply. "
        "Then inspect result.messages to see the tool-call lifecycle."
    )


async def main_async() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--create", action="store_true", help="Verify agent configuration")
    parser.add_argument("--chat", help="Send a single message to the agent")
    args = parser.parse_args()

    if args.create:
        await create_agent()
    elif args.chat:
        await chat_once(args.chat)
    else:
        parser.print_help()


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
