"""Ridge Analyst — Portfolio Analyst agent.

Wired end-to-end in exercises 4 + 5. Owns portfolio-positions / historical-returns
/ rebalance-simulator tools; explains allocation and performance decisions to
Ridgevault advisors in numbers-first prose.
"""
from __future__ import annotations
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


# TODO (exercise 4): implement get_portfolio_positions as a stub tool.
# Return a small, plausible portfolio for client "4471" as a list of {ticker, shares, market_value}.
def get_portfolio_positions(client_id: str) -> list[dict]:
    raise NotImplementedError("Exercise 4 wires this stub tool.")


# TODO (exercise 4): build the AIProjectClient + OpenAI-shape client, register
# get_portfolio_positions as a tool, and return a wired agent that answers
# Ridgevault portfolio questions.
def build_portfolio_analyst():
    raise NotImplementedError("Exercise 4 wires the agent.")


# TODO (exercise 5): call build_portfolio_analyst() and ask a real Ridgevault question
# such as "What's the current market value of client 4471's portfolio?" Print the answer.
def main() -> int:
    load_dotenv()
    if not os.environ.get("FOUNDRY_PROJECT_ENDPOINT") or not os.environ.get("FOUNDRY_MODEL"):
        print("ERROR: run verify_env.py first — .env is not populated.")
        return 1
    raise NotImplementedError("Exercise 5 drives the wired agent with a Ridgevault question.")


if __name__ == "__main__":
    raise SystemExit(main())
