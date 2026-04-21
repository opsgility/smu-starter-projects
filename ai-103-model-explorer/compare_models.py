"""
AI-103 Lesson 2 — Exercise 1
Benchmark three Foundry model deployments on the same prompt.

Usage:
    python compare_models.py "Summarize Azure AI Foundry in one sentence."

Environment (loaded from .env):
    AZURE_AI_PROJECT_ENDPOINT  Foundry project endpoint
                               (https://<hub>.services.ai.azure.com/api/projects/<project>)
    MODEL_DEPLOYMENTS          Comma-separated deployment names
                               (e.g. gpt-4.1-mini,gpt-4o,gpt-4.1-nano)
"""

from __future__ import annotations

import os
import sys
import time
from typing import Iterable

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()

DEFAULT_PROMPT = "Summarize Azure AI Foundry in one sentence."


def deployments() -> Iterable[str]:
    """Return the list of deployment names from the MODEL_DEPLOYMENTS env var."""
    raw = os.environ.get("MODEL_DEPLOYMENTS", "")
    names = [n.strip() for n in raw.split(",") if n.strip()]
    if not names:
        raise RuntimeError(
            "MODEL_DEPLOYMENTS is not set. Populate .env from the ARM template outputs "
            "(see Exercise 1, step 6)."
        )
    return names


def main() -> int:
    prompt = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PROMPT

    endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT")
    if not endpoint:
        raise RuntimeError(
            "AZURE_AI_PROJECT_ENDPOINT is not set. Populate .env from the ARM template "
            "outputs (see Exercise 1, step 6)."
        )

    console = Console()
    table = Table(title=f"Model comparison — prompt: {prompt!r}")
    table.add_column("deployment", style="cyan", no_wrap=True)
    table.add_column("latency (s)", justify="right")
    table.add_column("input tok", justify="right")
    table.add_column("output tok", justify="right")
    table.add_column("preview (first 80 chars)", overflow="fold")

    # AIProjectClient talks to the Foundry project; get_openai_client() hands back
    # an openai client preconfigured with the project's base URL + auth headers so
    # we can call the Responses API directly.
    with DefaultAzureCredential() as credential:
        with AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
            with project_client.get_openai_client() as client:
                for name in deployments():
                    # TODO (Exercise 1, Step 9, TODO 1): record a wall-clock start
                    # time with time.perf_counter() so we can measure latency.
                    #
                    # TODO (Exercise 1, Step 9, TODO 2): call the Responses API
                    # with client.responses.create(model=name, input=prompt) and
                    # read response.usage + response.output_text.
                    #
                    # TODO (Exercise 1, Step 9, TODO 3): append a row to the Rich
                    # table containing the deployment name, elapsed seconds,
                    # input_tokens, output_tokens, and an 80-char preview.
                    raise NotImplementedError(
                        "Finish the three TODOs in compare_models.py (Exercise 1, step 9)."
                    )

    console.print(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
