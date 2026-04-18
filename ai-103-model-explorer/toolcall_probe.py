"""Probe which deployments support function / tool calling.

Sends a prompt that SHOULD trigger the `get_weather` tool. If the model returns a
tool call, mark supported; otherwise mark unsupported.
"""
import json
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

load_dotenv()
console = Console()

TOOLS = [{
    "type": "function",
    "name": "get_weather",
    "description": "Return the current weather for a city",
    "parameters": {
        "type": "object",
        "properties": {"city": {"type": "string"}},
        "required": ["city"],
    },
}]

PROBE = "What's the weather in Seattle right now?"


def probe() -> None:
    endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    deployments = [d.strip() for d in os.environ["MODEL_DEPLOYMENTS"].split(",") if d.strip()]

    with AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential()) as project:
        with project.get_openai_client() as client:
            table = Table(title="Tool-calling support probe")
            table.add_column("Deployment")
            table.add_column("Supports tool calling?")
            table.add_column("Tool call (if any)")

            for name in deployments:
                # TODO 1: call client.responses.create(model=name, input=PROBE, tools=TOOLS).
                # TODO 2: inspect response.output for any item where item.type == "function_call".
                # TODO 3: add a row — "yes" with json.dumps({"name": item.name, "args": item.arguments})
                #         or "no" with "" if no tool call was produced.
                raise NotImplementedError

            console.print(table)


if __name__ == "__main__":
    probe()
