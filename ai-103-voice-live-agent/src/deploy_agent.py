"""Exercise 2 (part 2) — deploy the Foundry hosted agent.

Creates a Microsoft Foundry agent that answers Summitline product
questions from the AI Search index built by index_product_docs.py.
The agent is stateless — Voice Live will invoke it per turn.

Prints the agent id + name; write them into .env for the Voice Live client.
"""
from __future__ import annotations

import os
import sys

from azure.ai.agents.models import AzureAISearchTool
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

AGENT_NAME = "summitline-product-agent"
AGENT_INSTRUCTIONS = """\
You are the Summitline Outfitters product assistant. A store associate is
talking to you hands-free while helping a customer. Answer briefly (1-3
sentences), factually, and only from the product docs the AI Search tool
returns. If the docs don't cover the question, say "I don't have that in my
docs — I'd check with a store manager." Never invent SKUs, colors, weights,
or prices. When a customer asks about stock, tell the associate to check
the inventory tool — you cannot check stock yourself unless the tool is
provided in this turn.
"""


def main() -> int:
    endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    model = os.environ["MODEL_DEPLOYMENT"]

    cred = DefaultAzureCredential()
    project = AIProjectClient(endpoint=endpoint, credential=cred)

    # Wire the AI Search tool to the index the previous script populated.
    # The Foundry project must have an AI Search connection named exactly
    # as the resource — the ARM template at lab start creates that
    # connection for you.
    search_conn = project.connections.get_default(connection_type="AzureAISearch")
    search_tool = AzureAISearchTool(
        index_connection_id=search_conn.id,
        index_name=os.environ["AZURE_SEARCH_INDEX_NAME"],
    )

    # Delete any leftover agent from a previous run — the name is the
    # convention for this lab.
    for a in project.agents.list_agents():
        if a.name == AGENT_NAME:
            print(f"Deleting stale agent {a.id}")
            project.agents.delete_agent(a.id)

    agent = project.agents.create_agent(
        model=model,
        name=AGENT_NAME,
        instructions=AGENT_INSTRUCTIONS,
        tools=search_tool.definitions,
        tool_resources=search_tool.resources,
    )
    print(f"Created agent {agent.id}  (name={agent.name}, model={model})")
    print("Export this into your shell so voice_live_client.py picks it up:")
    print(f'  export AZURE_AI_AGENT_ID="{agent.id}"')
    print(f'  export AZURE_AI_AGENT_NAME="{agent.name}"')
    return 0


if __name__ == "__main__":
    sys.exit(main())
