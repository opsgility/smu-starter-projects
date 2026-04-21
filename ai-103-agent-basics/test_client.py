"""Smoke test for the Summitline Outfitters concierge agent.

Runs a 3-turn conversation through ``converse()`` and prints a role-tagged
transcript. Each turn is crafted to force a specific function tool to fire:

1. ``get_weather`` (Bend shipping weather)
2. ``calculate``   (bulk-order math)
3. ``lookup_inventory`` (NW-SL-001 stock check)

Exercise 3 Step 2 asks you to append a fourth turn that exercises two tools
in a single message.
"""
from __future__ import annotations

from app.agent import converse


CONVO = [
    "Hi! What's the weather in Bend?",
    "What's 47 * 12?",
    "Do we have any NW-SL-001 in stock?",
]


def main() -> None:
    transcript = converse(CONVO)
    for turn in transcript:
        role = turn.get("role", "?").upper()
        text = turn.get("text", "")
        print(f"{role:<9} | {text}")


if __name__ == "__main__":
    main()
