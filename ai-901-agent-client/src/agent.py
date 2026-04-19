"""Foundry single-agent starter."""
from __future__ import annotations

import argparse
import json
import os

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FunctionTool, ToolSet
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
DEPLOYMENT = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")
AGENT_ID = os.environ.get("AGENT_ID")


def get_store_hours(store_id: str) -> str:
    """Return the hours for a store — exercise has you replace the hard-coded map."""
    hours = {"42": "Mon–Sat 9–9, Sun 11–6", "17": "Mon–Fri 8–8, weekends closed"}
    return json.dumps({"store_id": store_id, "hours": hours.get(store_id, "unknown")})


def build_client() -> AgentsClient:
    if not ENDPOINT:
        raise RuntimeError("Set FOUNDRY_PROJECT_ENDPOINT in .env.")
    return AgentsClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())


def create_agent() -> str:
    client = build_client()
    toolset = ToolSet()
    toolset.add(FunctionTool({get_store_hours}))
    agent = client.create_agent(
        model=DEPLOYMENT,
        name="northwind-store-assistant",
        instructions=(
            "You are a helpful in-store assistant for Northwind Horizon. "
            "When asked about store hours, call the get_store_hours tool. "
            "Be concise."
        ),
        toolset=toolset,
    )
    print(f"Created agent: {agent.id}")
    print("Put that ID into .env as AGENT_ID for the chat step.")
    return agent.id


def chat_once(message: str) -> None:
    """TODO (exercise): implement thread + run for the configured AGENT_ID."""
    raise NotImplementedError(
        "Exercise step: create thread, post message, create run, poll until terminal, print reply."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--create", action="store_true", help="Create the agent")
    parser.add_argument("--chat", help="Send a single message to AGENT_ID")
    args = parser.parse_args()

    if args.create:
        create_agent()
    elif args.chat:
        if not AGENT_ID:
            raise SystemExit("Set AGENT_ID in .env first (run --create or use portal).")
        chat_once(args.chat)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
