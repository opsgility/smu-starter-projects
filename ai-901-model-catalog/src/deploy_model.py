"""Stub for deploying a model via the Foundry SDK.

The exercise first walks you through creating a deployment in the portal
(Deployments → Deploy model → Deploy base model → pick gpt-4o-mini),
then has you replicate the same deployment here via code.
"""
from __future__ import annotations

import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
DEPLOYMENT_NAME = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")


def deploy_chat_model(model_name: str = "gpt-4o-mini") -> None:
    """TODO (exercise): call client.deployments.create() with the right model / sku / capacity."""
    raise NotImplementedError(
        "Exercise: call client.deployments.create() for a base chat model. "
        "Match what you deployed in the portal in step 3."
    )


def main() -> None:
    if not ENDPOINT:
        raise RuntimeError("Set FOUNDRY_PROJECT_ENDPOINT in .env.")
    _ = AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())
    deploy_chat_model()


if __name__ == "__main__":
    main()
