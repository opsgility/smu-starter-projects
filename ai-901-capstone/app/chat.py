"""Wrap the Foundry chat model for the capstone /chat endpoint."""
import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ.get("CHAT_DEPLOYMENT", "ai901-chat")

SYSTEM = (
    "You are Northwind Horizon's concierge. "
    "Be concise, brand-friendly, and suggest no more than three products per reply."
)


def reply(message: str) -> str:
    # TODO 1: Build ChatCompletionsClient and send SystemMessage(SYSTEM) + UserMessage(message).
    # TODO 2: Return response.choices[0].message.content.
    raise NotImplementedError
