# Lesson 10 helper. Reads data/golden-inputs.txt one prompt per line, runs each
# through the current Halcyon Assist agent, and writes the golden JSONL.
from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from copilot_agent import build_agent


# Both paths resolve relative to the repository root (parent of src/).
REPO_ROOT = Path(__file__).resolve().parent.parent
INPUTS_PATH = REPO_ROOT / "data" / "golden-inputs.txt"
OUTPUT_PATH = REPO_ROOT / "data" / "aurora-eval-golden.jsonl"


def load_inputs(path: Path) -> list[str]:
    """Return non-empty, non-comment lines from the golden-inputs file."""
    if not path.exists():
        return []
    lines = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append(stripped)
    return lines


async def capture(prompt: str) -> dict:
    """Run one prompt through Halcyon Assist and return an eval-shaped record."""
    agent = build_agent()
    thread = agent.get_new_thread()
    result = await agent.run(prompt, thread=thread)
    reply = str(result)
    # 'context' will be replaced by real retrieved policy text once Lesson 6
    # attaches the AI Search tool. Leave a stub so the eval SDK schema stays valid.
    return {"query": prompt, "response": reply, "context": ""}


async def _main() -> None:
    load_dotenv()

    inputs = load_inputs(INPUTS_PATH)
    if not inputs:
        print(
            f"[capture_golden] {INPUTS_PATH} is empty. Add one prompt per line "
            f"during Lesson 10 Exercise 1, then re-run."
        )
        return

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        for prompt in inputs:
            record = await capture(prompt)
            handle.write(json.dumps(record) + "\n")
            print(f"[capture_golden] captured: {prompt[:60]}")

    print(f"[capture_golden] wrote {len(inputs)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(_main())
