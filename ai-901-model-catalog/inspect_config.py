"""
Inspect deployment configuration parameters for a Foundry deployment.

Print the SKU, capacity, scale settings, RAI filter, and endpoint.
"""
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
DEPLOYMENT_NAME = "ai901-chat"


def inspect() -> None:
    client = AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())

    # TODO 1: fetch the deployment by name and print:
    #         - model.name, model.version, model.publisher
    #         - sku.name, sku.capacity
    #         - scale_settings.scale_type
    #         - rai_policy_name (content filter policy name)
    #         - inference endpoint URL
    raise NotImplementedError


if __name__ == "__main__":
    inspect()
