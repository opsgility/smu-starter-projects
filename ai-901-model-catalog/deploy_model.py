"""
Deploy a selected model to your Foundry project.

The exercise uses `gpt-4o-mini` by default. Students adapt to deploy any model
of their choice.
"""
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
DEPLOYMENT_NAME = "ai901-chat"
MODEL_NAME = "gpt-4o-mini"
MODEL_VERSION = "2024-07-18"


def deploy() -> None:
    client = AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())

    # TODO 1: call client.deployments.begin_create_or_update(...) with:
    #         - name=DEPLOYMENT_NAME
    #         - model={"name": MODEL_NAME, "version": MODEL_VERSION, "publisher": "OpenAI"}
    #         - sku={"name": "Standard", "capacity": 10}
    # TODO 2: wait for the long-running operation and print the final status.
    raise NotImplementedError


if __name__ == "__main__":
    deploy()
