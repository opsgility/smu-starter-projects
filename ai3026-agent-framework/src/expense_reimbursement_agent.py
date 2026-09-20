"""Halcyon expense reimbursement categorization agent — Microsoft Agent Framework.

Complete the TODO markers as you work through Lesson 10.
"""
from __future__ import annotations
import asyncio
import json
import os
from pathlib import Path

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "expenses.json"


HALCYON_EXPENSE_RULES = """\
Halcyon Insurance adjuster expense reimbursement rules (fictional, for training use):

  - Categories: 'mileage', 'meals', 'lodging', 'other'.
  - Mileage: reimbursed at $0.67 per mile. No receipt required.
  - Meals: per-diem cap of $65/day; anything over requires a receipt AND a note explaining the overage.
  - Lodging: reimbursed at actual cost, receipt required for any amount. Cap of $250/night in tier-1 cities,
    $175/night elsewhere.
  - 'Other' expenses require both a receipt and a written justification.
  - Any line item over $500 also requires a manager pre-approval reference in the notes field.

For each expense line, respond with:
  1. Category
  2. Whether it is APPROVED, HOLD_FOR_RECEIPT, HOLD_FOR_JUSTIFICATION, or ESCALATE_TO_MANAGER
  3. A one-sentence explanation an adjuster can paste back into the expense tool.
"""


async def main() -> None:
    load_dotenv()
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model = os.environ["FOUNDRY_MODEL"]

    # TODO (Ex 2): instantiate FoundryChatClient with the endpoint, model, and
    # DefaultAzureCredential.
    client: FoundryChatClient = ...  # type: ignore[assignment]

    # TODO (Ex 2): construct the Agent with:
    #   name="HalcyonExpenseHelper"
    #   instructions=HALCYON_EXPENSE_RULES
    # Optionally add a system prompt prefix explaining the Halcyon Assist context.
    agent: Agent = ...  # type: ignore[assignment]

    # Load the 5 test expenses.
    with DATA_FILE.open() as fh:
        expenses = json.load(fh)

    # TODO (Ex 3): for each expense, call agent.run(...) and print the response.
    # Non-streaming for the first pass — clean text output.
    for expense in expenses:
        prompt = f"Adjuster expense line: {json.dumps(expense)}"
        print(f"\n=== {expense['description']} ===")
        # TODO — send prompt, print response.

    # TODO (Ex 4): add streaming with agent.run_stream(...) — pick ONE of the 5
    # expenses and print the response token-by-token.

    # TODO (Ex 5): add multi-turn conversation state using Thread. Simulate an
    # adjuster asking "what if I add a receipt for the meal overage?" as a
    # follow-up to a HOLD_FOR_RECEIPT verdict.


if __name__ == "__main__":
    asyncio.run(main())
