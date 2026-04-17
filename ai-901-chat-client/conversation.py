"""
Multi-turn chat — keep the conversation history in memory and stream
back model responses. Quit with 'exit'.
"""
import os

from azure.ai.projects import AIProjectClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ.get("DEPLOYMENT_NAME", "ai901-chat")

SYSTEM_PROMPT = "You are a helpful assistant for Northwind Horizon."


def main() -> None:
    project = AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())
    chat_client = project.inference.get_chat_completions_client()

    history = [SystemMessage(SYSTEM_PROMPT)]

    while True:
        user = input("You: ").strip()
        if user.lower() in {"exit", "quit"}:
            break

        # TODO 1: append UserMessage(user) to history.
        # TODO 2: call chat_client.complete(model=DEPLOYMENT, messages=history).
        # TODO 3: capture the assistant reply, print it, and append AssistantMessage(reply) to history.
        raise NotImplementedError


if __name__ == "__main__":
    main()
