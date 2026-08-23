"""Ridgevault compliance_officer agent — consumes the SAME hosted MCP tools.

Same HostedMCPTool wiring as investment_researcher.py — that's the whole point
of MCP: one hosted tool server, N agents. Complete the TODOs as you work
through Exercise 5.
"""
from __future__ import annotations
import asyncio
import os

from agent_framework import HostedMCPTool
from agent_framework.foundry import FoundryChatClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv


AGENT_SYSTEM_PROMPT = """You are Ridge Compliance, Ridgevault Financial's compliance_officer agent.

Your job: given a proposed trade (issuer, sector, notional in USD), decide whether
Ridgevault's per-issuer AND per-sector limits allow the trade. ALWAYS call
`check_position_limit` before returning a verdict. If the tool says allowed=False,
quote its `reason` field verbatim so the advisor understands why.

You MAY also call `get_market_snapshot` if the user's proposed notional is expressed
in shares rather than USD and you need `last_close` to convert. Otherwise leave the
market snapshot to the investment_researcher agent.
"""


async def main() -> None:
    load_dotenv()
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model = os.environ["FOUNDRY_MODEL"]
    mcp_url = f"{os.environ['FUNCTION_APP_URL'].rstrip('/')}/api/mcp"

    # TODO (Ex 5): construct a HostedMCPTool pointing at `mcp_url` — same shape
    # as investment_researcher.py. Ridgevault deliberately re-uses one tool server
    # across both agents.
    tool: HostedMCPTool = ...  # type: ignore[assignment]

    async with AzureCliCredential() as credential:
        chat_client = FoundryChatClient(
            project_endpoint=endpoint,
            model=model,
            credential=credential,
        )

        # TODO (Ex 5): create the compliance agent and run this question.
        question = (
            "A client wants to buy $2,500,000 of Apple Inc. (Information Technology "
            "sector). Are we inside Ridgevault's per-issuer and per-sector limits?"
        )
        print(f"\n>>> USER: {question}\n")
        # response = await agent.run(question)
        # print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
