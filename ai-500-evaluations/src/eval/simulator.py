"""Exercise 4 — Synthetic test-case generation with the Foundry Simulator.

Uses `azure.ai.evaluation.simulator.Simulator` to generate N additional
Ridgevault-style portfolio-review queries + contexts, appends them to a fresh
`data/synth-test-set-portfolio-reviews.jsonl`, and prints a preview of the
first 3 rows.

Exercise task: raise SYNTH_COUNT and rerun; then feed the synthetic file into
run_builtin_evaluators.py by pointing TEST_SET at it (or by adding a --path
flag as a stretch task).
"""
from __future__ import annotations
import asyncio
import json
import os
import sys
from pathlib import Path

from azure.ai.evaluation.simulator import Simulator
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

OUT_PATH = Path(__file__).resolve().parents[2] / "data" / "synth-test-set-portfolio-reviews.jsonl"
SYNTH_COUNT = 6  # small default so the exercise runs in under a minute

SEED_TOPICS = [
    "quarterly performance summary for a taxable account with a technology overweight",
    "tax-loss harvesting recommendation with wash-sale considerations",
    "explanation of a recent rebalance triggered by a drift band breach",
    "asset-allocation review versus a 60/40 target",
    "bond ladder maturities and reinvestment plan",
    "Roth conversion analysis for a client approaching retirement",
]


async def _simulate_one(sim: Simulator, model: str, topic: str) -> dict:
    # Simulator returns a conversation list; we take the last user turn as the
    # synthetic "query" and the assistant turn's cited context as "context".
    convo = await sim(
        target=lambda messages, **_: {
            "messages": messages + [
                {"role": "assistant", "content": f"Draft Ridgevault portfolio-review reply about {topic}."}
            ]
        },
        model_config={
            "azure_endpoint": os.environ["FOUNDRY_PROJECT_ENDPOINT"].split("/api/projects/")[0],
            "azure_deployment": model,
            "api_version": "2025-04-01-preview",
        },
        max_conversation_turns=2,
        tasks=[f"A Ridgevault client asks about: {topic}"],
    )
    return {
        "id": f"synth-{topic[:20].replace(' ', '-')}",
        "query": convo[-1].get("content", "") if convo else "",
        "context": f"Ridgevault account excerpt for '{topic}'.",
        "ground_truth": "",
    }


async def main_async() -> int:
    load_dotenv()
    sim = Simulator(credential=DefaultAzureCredential())
    model = os.environ["FOUNDRY_MODEL"]

    rows: list[dict] = []
    for topic in SEED_TOPICS[:SYNTH_COUNT]:
        rows.append(await _simulate_one(sim, model, topic))
        print(f"  synthesized: {topic}")

    OUT_PATH.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    print()
    print(f"Wrote {len(rows)} synthetic test cases to {OUT_PATH}")
    print("Preview:")
    for row in rows[:3]:
        print(f"  {row['id']}: {row['query'][:80]}...")
    return 0


def main() -> int:
    return asyncio.run(main_async())


if __name__ == "__main__":
    sys.exit(main())
