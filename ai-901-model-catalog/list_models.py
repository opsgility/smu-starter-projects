"""
List and filter models in the Microsoft Foundry catalog.

Students complete the TODOs to print:
- all models in the catalog
- models filtered by publisher (e.g., Microsoft, OpenAI)
- models filtered by task (chat-completion, embeddings, image-generation)
"""
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]


def get_client() -> AIProjectClient:
    # TODO 1: create an AIProjectClient using DefaultAzureCredential() and the endpoint.
    raise NotImplementedError


def list_all_models(client: AIProjectClient) -> None:
    """Print every model's id, publisher, and primary task."""
    # TODO 2: iterate client.models.list() and print name + publisher + task.
    raise NotImplementedError


def filter_by_publisher(client: AIProjectClient, publisher: str) -> list[str]:
    """Return the model names published by the given publisher."""
    # TODO 3: filter the catalog to only models where model.publisher == publisher.
    raise NotImplementedError


def filter_by_task(client: AIProjectClient, task: str) -> list[str]:
    """Return model names that support the given task (e.g. 'chat-completion')."""
    # TODO 4: filter by task capability; return the list.
    raise NotImplementedError


if __name__ == "__main__":
    client = get_client()
    list_all_models(client)
    print("\nMicrosoft models:", filter_by_publisher(client, "Microsoft"))
    print("Chat completion models:", filter_by_task(client, "chat-completion"))
