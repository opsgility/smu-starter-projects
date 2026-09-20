"""Exercise 2 + 3 — Sequential portfolio-review pipeline via Microsoft Agent Framework.

Build a SequentialBuilder pipeline over the four specialists so they run in order
on ONE shared conversation thread:

  portfolio_analyst -> risk_assessor -> compliance_officer -> brief_writer

You fill in the TODO block. Then run:

    python -m src.orchestrators.sequential_builder data/test-portfolio.json

The final message the workflow emits IS the morning brief you send to the
advisor.
"""
from __future__ import annotations
import asyncio
import json
import os
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from src.agents import (
    portfolio_analyst,
    risk_assessor,
    compliance_officer,
    brief_writer,
)


async def run(portfolio_path: str) -> str:
    load_dotenv()
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model = os.environ["FOUNDRY_MODEL"]
    project = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())

    with open(portfolio_path, "r", encoding="utf-8") as fh:
        portfolio = json.load(fh)

    # Build the four specialists.
    analyst = portfolio_analyst.build_agent(project, model)
    risk = risk_assessor.build_agent(project, model)
    compliance = compliance_officer.build_agent(project, model)
    writer = brief_writer.build_agent(project, model)

    # TODO (exercise 2):
    #   1. Import SequentialBuilder from agent_framework.
    #   2. Compose the four agents in order into a workflow — analyst, risk, compliance, writer.
    #   3. Kick it off with the portfolio JSON as the seed message.
    #   4. Return the final assistant message text.
    #
    # Reference pattern:
    #     from agent_framework import SequentialBuilder
    #     workflow = SequentialBuilder().participants([analyst, risk, compliance, writer]).build()
    #     result = await workflow.run(f"Portfolio JSON:\n{json.dumps(portfolio)}")
    #     return result.final_message.text
    raise NotImplementedError("Complete the SequentialBuilder wiring per exercise 2.")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/test-portfolio.json"
    print(asyncio.run(run(path)))
