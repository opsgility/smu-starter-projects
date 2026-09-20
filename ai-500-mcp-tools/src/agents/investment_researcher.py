"""Ridgevault investment_researcher agent — consumes the hosted MCP tools.

Complete the TODOs as you work through Exercise 5. The agent uses
`HostedMCPTool` (Microsoft Agent Framework) to point at the deployed Function
App's MCP endpoint. The runtime performs the MCP `tools/list` handshake for
you — every advertised tool becomes callable with no per-tool wiring in this
file.
"""
from __future__ import annotations
import asyncio
import os

from agent_framework import HostedMCPTool
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv


AGENT_SYSTEM_PROMPT = """You are Ridge Research, Ridgevault Financial's investment_researcher agent.

Your job: given a client's portfolio question, look up the current market snapshot for
the tickers involved and draft a two-paragraph research brief. When the user names
one or more tickers, ALWAYS call `get_market_snapshot` before drafting your reply.
Never invent price, volume, or day-change data — if a ticker comes back under
`not_covered`, say so plainly.

Do NOT call `check_position_limit` — that tool belongs to the compliance_officer
agent, not you. If the user asks whether a proposed trade is allowed, hand off to
compliance and stop.
"""


async def main() -> None:
    load_dotenv()
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model = os.environ["FOUNDRY_MODEL"]
    mcp_url = f"{os.environ['FUNCTION_APP_URL'].rstrip('/')}/api/mcp"

    # TODO (Ex 5): construct a HostedMCPTool pointing at `mcp_url`.
    # Give it a stable `name` like "ridgevault_tools" — the model uses that label
    # when planning tool calls.
    tool: HostedMCPTool = ...  # type: ignore[assignment]

    async with AzureCliCredential() as credential:
        chat_client = FoundryChatClient(
            project_endpoint=endpoint,
            model=model,
            credential=credential,
        )

        # TODO (Ex 5): create an agent from `chat_client` with:
        #   - instructions=AGENT_SYSTEM_PROMPT
        #   - tools=[tool]
        # Then send this question and print the final response.
        question = (
            "Give me a quick research brief on AAPL and MSFT for a client who is "
            "worried about tech-sector volatility."
        )
        print(f"\n>>> USER: {question}\n")
        # response = await agent.run(question)
        # print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
