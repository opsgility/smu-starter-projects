"""Halcyon repair-estimate agent — Foundry agent that consumes the local MCP server.

Complete the TODO markers as you work through Lesson 6.
"""
from __future__ import annotations
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPTool, PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model = os.environ["FOUNDRY_MODEL"]
    mcp_url = os.environ.get("MCP_SERVER_URL", "http://127.0.0.1:8123/mcp")

    # TODO (Ex 3): instantiate AIProjectClient with DefaultAzureCredential.
    client: AIProjectClient = ...  # type: ignore[assignment]

    # TODO (Ex 3): register the MCP server as an MCPTool. This point the agent at the
    # fastmcp server running in the other terminal — the agent auto-discovers the two
    # tools (lookup_part, estimate_repair_cost) via the MCP handshake.
    tool: MCPTool = ...  # type: ignore[assignment]

    # TODO (Ex 3): build a PromptAgentDefinition. System prompt should tell the agent
    # it is Halcyon's repair-estimate assistant and it should call lookup_part when
    # the user mentions a part number and estimate_repair_cost when they mention a
    # claim ID.
    definition: PromptAgentDefinition = ...  # type: ignore[assignment]

    # TODO (Ex 4): create the agent, then send these three test prompts and print
    # each response:
    test_prompts = [
        "What does Halcyon-approved part 47B-991 cost, and what's the total repair estimate on claim CLM-2026-091502?",
        "How much are we looking at for claim CLM-2026-091504?",
        "What's the story on part XYZ-9999?  (should trigger the 'not in catalog' branch)",
    ]

    for prompt in test_prompts:
        print(f"\n===\n{prompt}\n===")
        # TODO — send prompt, print final response, then also print the tool_call trace
        # so you can see which MCP tools fired.


if __name__ == "__main__":
    main()
