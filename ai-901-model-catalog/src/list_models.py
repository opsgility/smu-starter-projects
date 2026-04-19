"""List deployments in the configured Foundry project."""
from __future__ import annotations

import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
if not ENDPOINT:
    raise RuntimeError("Set FOUNDRY_PROJECT_ENDPOINT in .env (see .env.example).")


def main() -> None:
    client = AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())
    rows = list(client.deployments.list())
    if not rows:
        print("No deployments yet — the exercise has you create one.")
        return
    print(f"{'deployment':<30} {'model':<25} {'type':<15} sku")
    print("-" * 90)
    for d in rows:
        name = getattr(d, "name", "?")
        model = getattr(d, "model_name", getattr(d, "model", "?"))
        typ = getattr(d, "type", "?")
        sku = getattr(d, "sku", "?")
        print(f"{name:<30} {model!s:<25} {typ!s:<15} {sku!s}")


if __name__ == "__main__":
    main()
