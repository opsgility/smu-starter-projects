"""
Single-turn chat — send one user message to a Foundry-deployed model
and print the response.
"""
import os
import sys

from azure.ai.projects import AIProjectClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ.get("DEPLOYMENT_NAME", "ai901-chat")

SYSTEM_PROMPT = (
    "You are a helpful assistant for Northwind Horizon. "
    "Keep answers under 3 sentences."
)


def chat(user_text: str) -> str:
    project = AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())

    # TODO 1: get a chat-completions client from the project:
    #         chat_client = project.inference.get_chat_completions_client()
    # TODO 2: call chat_client.complete(
    #             model=DEPLOYMENT,
    #             messages=[SystemMessage(SYSTEM_PROMPT), UserMessage(user_text)]
    #         )
    # TODO 3: return response.choices[0].message.content
    raise NotImplementedError


def main() -> None:
    query = " ".join(sys.argv[1:]) or "Give me a quick product idea for Father's Day."
    print(chat(query))


if __name__ == "__main__":
    main()
