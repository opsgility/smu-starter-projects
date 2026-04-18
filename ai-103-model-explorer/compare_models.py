"""Compare every deployment listed in MODEL_DEPLOYMENTS on the same prompt."""
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
console = Console()


def deployments() -> Iterable[str]:
    return [d.strip() for d in os.environ["MODEL_DEPLOYMENTS"].split(",") if d.strip()]


def run(prompt: str) -> None:
    endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    with AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential()) as project:
        with project.get_openai_client() as client:
            table = Table(title=f"Prompt: {prompt}")
            table.add_column("Deployment")
            table.add_column("Latency (s)")
            table.add_column("Input tokens")
            table.add_column("Output tokens")
            table.add_column("First 80 chars")

            for name in deployments():
                # TODO 1: wrap the call in time.perf_counter() to measure latency.
                # TODO 2: call client.responses.create(model=name, input=prompt) and capture response.
                # TODO 3: append a row: name, f"{elapsed:.2f}", usage.input_tokens,
                #         usage.output_tokens, response.output_text[:80].
                raise NotImplementedError

            console.print(table)


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Summarize Azure AI Foundry in one sentence."
    run(prompt)
