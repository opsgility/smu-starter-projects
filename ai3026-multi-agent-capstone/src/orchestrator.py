"""Halcyon claims-triage orchestrator — SequentialBuilder pipeline.

Wires three specialists into one pipeline:
  1. coverage_agent (local)               — verifies coverage
  2. damage_assessment (REMOTE via A2A)   — assesses damage severity + cost band
  3. adjuster_brief_agent (local)         — drafts the adjuster's first-touch brief

The damage_assessment step is discovered dynamically via the A2A AgentCard at
DAMAGE_A2A_URL/.well-known/agent.json.

Complete the TODO markers as you work through Lesson 12.
"""
from __future__ import annotations
import asyncio
import json
import os
from pathlib import Path

from agent_framework import SequentialBuilder
from dotenv import load_dotenv

from specialists.coverage_agent import build_coverage_agent
from specialists.adjuster_brief_agent import build_adjuster_brief_agent


TEST_CLAIM_FILE = Path(__file__).resolve().parents[1] / "data" / "test-claim.json"


async def main() -> None:
    load_dotenv()
    damage_url = os.environ.get("DAMAGE_A2A_URL", "http://127.0.0.1:8500")

    # Build the two local specialists.
    coverage = build_coverage_agent()
    adjuster_brief = build_adjuster_brief_agent()

    # TODO (Ex 3): discover the remote damage-assessment agent via its AgentCard.
    # The a2a-sdk client typically exposes something like:
    #   from a2a.client import A2AClient
    #   remote_damage = await A2AClient.from_agent_card_url(f"{damage_url}/.well-known/agent.json")
    # Then wrap it so SequentialBuilder can call it in the same shape as local agents.
    # Check the lab agent's cheat sheet for the current signature.
    remote_damage = ...  # type: ignore[assignment]

    # TODO (Ex 3): build the SequentialBuilder pipeline. Order:
    #   coverage -> remote_damage -> adjuster_brief
    # Each downstream stage receives the concatenated context from the previous stages.
    pipeline = ...  # type: ignore[assignment]

    # Load the test claim.
    with TEST_CLAIM_FILE.open() as fh:
        claim = json.load(fh)

    # TODO (Ex 4): run the pipeline on the test claim. Print each stage's output
    # for the write-up.
    prompt = f"Halcyon claim payload:\n{json.dumps(claim, indent=2)}"
    print(f"\n=== Kicking off pipeline for claim {claim['claim_id']} ===\n")
    # TODO — invoke pipeline, iterate results, print stage-by-stage output.

    # TODO (Ex 6 — CAPSTONE CHALLENGE): re-run the pipeline after killing the A2A
    # server in Terminal 1 (Ctrl+C). Observe how the orchestrator handles the failure.
    # Options:
    #   - fallback to a local damage-assessment agent
    #   - surface the failure to the adjuster with a "damage_assessment offline" flag
    #   - retry with backoff
    # Pick one approach and implement it. Write up your choice in the lab notes.


if __name__ == "__main__":
    asyncio.run(main())
