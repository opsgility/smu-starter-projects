"""Exercises 4 + 5 + 6 — Same portfolio-review flow as a LangGraph StateGraph.

Rebuild the sequential pipeline as a typed graph with per-node state so you feel
the difference. Add a human-in-the-loop approval gate at the compliance node
(exercise 5). In exercise 6 you fault-inject one specialist and add graceful
degradation via an on-graph error edge.

The graph shape after exercise 4:

    START -> analyst -> risk -> compliance -> brief -> END

After exercise 5 you add an interrupt() inside the compliance node so the graph
pauses waiting for a human approval, resumable via Command(resume="approve"|"reject").
"""
from __future__ import annotations
import asyncio
import json
import os
import sys
from typing import TypedDict, Optional

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


class ReviewState(TypedDict, total=False):
    """State the graph passes node-to-node.

    Every node reads what it needs and writes exactly one field.
    """
    portfolio: dict
    analyst_read: str
    risk_summary: str
    compliance_verdict: str      # "APPROVE" or "REJECT: <reason>"
    human_decision: Optional[str]  # populated by the HITL interrupt in exercise 5
    brief: str
    error: Optional[str]         # populated when a specialist fails (exercise 6)


async def run(portfolio_path: str) -> str:
    load_dotenv()
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model = os.environ["FOUNDRY_MODEL"]
    project = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())

    with open(portfolio_path, "r", encoding="utf-8") as fh:
        portfolio = json.load(fh)

    # TODO (exercise 4):
    #   1. Build a StateGraph(ReviewState) with 4 nodes (analyst, risk, compliance, brief).
    #   2. Each node calls its specialist agent and returns a state fragment.
    #   3. Wire START -> analyst -> risk -> compliance -> brief -> END.
    #   4. Compile with a MemorySaver checkpointer so exercise 5's interrupt()
    #      can pause/resume, then invoke with an initial state.
    #
    # TODO (exercise 5):
    #   Inside the compliance node, after the specialist emits its verdict,
    #   call langgraph.types.interrupt({"verdict": ..., "reason": ...}) so the
    #   graph pauses. Resume from stdin with Command(resume=<decision>).
    #
    # TODO (exercise 6):
    #   Add graceful degradation. Wrap each specialist call in try/except; on
    #   failure route to an "error" node that fills in state["error"] and jumps
    #   straight to a truncated brief so the workflow still completes.
    raise NotImplementedError("Complete the LangGraph StateGraph per exercises 4, 5, and 6.")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "data/test-portfolio.json"
    print(asyncio.run(run(path)))
