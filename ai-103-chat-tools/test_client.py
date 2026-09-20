"""Smoke test for the Summitline Outfitters chat API.

Run this with the FastAPI server already up on port 8000:

    uvicorn app.main:app --reload --port 8000    # terminal 1
    python test_client.py                         # terminal 2

It hits the three endpoints the exercises ask about:

1. ``POST /chat`` with a prompt that SHOULD trigger ``get_weather``.
2. ``POST /chat`` with a prompt that should NOT trigger any tool.
3. ``POST /chat/stream`` — prints ``delta`` payloads as they arrive.
"""

from __future__ import annotations

import json
import sys

import requests


BASE_URL = "http://127.0.0.1:8000"


def _chat(message: str) -> dict:
    """POST to /chat and return the parsed JSON response."""
    r = requests.post(f"{BASE_URL}/chat", data={"message": message}, timeout=120)
    r.raise_for_status()
    return r.json()


def _stream(message: str) -> None:
    """POST to /chat/stream and print each SSE delta as it arrives."""
    with requests.post(
        f"{BASE_URL}/chat/stream",
        data={"message": message},
        stream=True,
        timeout=120,
    ) as r:
        r.raise_for_status()
        for raw_line in r.iter_lines(decode_unicode=True):
            if not raw_line:
                continue
            if not raw_line.startswith("data:"):
                continue
            payload = raw_line[len("data:"):].strip()
            if payload == "[DONE]":
                print("\n[DONE]")
                return
            try:
                chunk = json.loads(payload)
            except json.JSONDecodeError:
                # Unexpected frame — print raw so the student can debug it.
                print(payload, end="", flush=True)
                continue
            delta = chunk.get("delta", "")
            print(delta, end="", flush=True)


def main() -> int:
    # 1. Tool-calling turn — expect a `get_weather` call
    print("/chat (tool call expected):")
    result = _chat("What's the weather in Seattle?")
    print(json.dumps(result, indent=2))
    print()

    # 2. Non-tool turn — expect `tool_calls` == []
    print("/chat (no tool expected):")
    result = _chat("Hi, give me a one-sentence greeting.")
    print(json.dumps(result, indent=2))
    print()

    # 3. Streaming turn
    print("/stream:")
    _stream("Explain RAG in two sentences for a Summitline staff member.")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
