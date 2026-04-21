"""
AI-103 Lesson 2 — Exercise 2
Probe each deployed model for tool-calling (function-calling) support.

Usage:
    python toolcall_probe.py

Environment (loaded from .env):
    AZURE_AI_PROJECT_ENDPOINT  Foundry project endpoint
    MODEL_DEPLOYMENTS          Comma-separated deployment names
"""

from __future__ import annotations

import json
import os
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

# The prompt we hand to every model. The question is ambiguous on purpose — a
# capable LLM will infer that the get_weather tool is the right way to answer
# it, while a small model may just answer in natural language.
PROBE = "What's the weather in Seattle right now?"

# Responses API tool schema — FLAT. No {"function": {...}} wrapper.
# type, name, description, parameters sit at the top level.
TOOLS = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Return the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    }
]


def _load_deployments() -> list[str]:
    raw = os.environ.get("MODEL_DEPLOYMENTS", "")
    names = [n.strip() for n in raw.split(",") if n.strip()]
    if not names:
        raise RuntimeError(
            "MODEL_DEPLOYMENTS is not set. Populate .env from the ARM template outputs "
            "(see Exercise 1, step 6)."
        )
    return names


def main() -> int:
    endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
    if not endpoint:
        raise RuntimeError(
            "AZURE_AI_PROJECT_ENDPOINT is not set. Populate .env from the ARM template "
            "outputs (see Exercise 1, step 6)."
        )

    deployments = _load_deployments()

    console = Console()
    table = Table(title=f"Tool-calling probe — prompt: {PROBE!r}")
    table.add_column("deployment", style="cyan", no_wrap=True)
    table.add_column("tool call?", justify="center")
    table.add_column("call detail", overflow="fold")

    with DefaultAzureCredential() as credential:
        with AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
            with project_client.get_openai_client() as client:
                for name in deployments:
                    # TODO (Exercise 2, Step 4, TODO 1): call the Responses API
                    # with client.responses.create(model=name, input=PROBE,
                    # tools=TOOLS). Wrap the call in try/except so a single
                    # model failure doesn't abort the whole probe — on
                    # Exception, add_row(name, "error", str(exc)[:60]) and
                    # continue.
                    #
                    # TODO (Exercise 2, Step 4, TODO 2): scan response.output
                    # for the first item whose type attribute equals
                    # "function_call" using
                    # next((item for item in response.output
                    #       if getattr(item, "type", None) == "function_call"),
                    #      None).
                    #
                    # TODO (Exercise 2, Step 4, TODO 3): if a call was found,
                    # add a "yes" row with a JSON-rendered {name, args} detail;
                    # otherwise add a "no" row.
                    raise NotImplementedError(
                        "Finish the three TODOs in toolcall_probe.py (Exercise 2, step 4)."
                    )

    console.print(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
