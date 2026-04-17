"""Multimodal image Q&A for /analyze-image."""
import base64
import os
from pathlib import Path

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    ImageContentItem,
    ImageUrl,
    SystemMessage,
    TextContentItem,
    UserMessage,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ.get("MULTIMODAL_DEPLOYMENT", "gpt-4o")


def _encode(path: Path) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def analyze(image_path: Path, question: str) -> dict:
    # TODO 1: build ChatCompletionsClient + user message containing TextContentItem(question)
    #         and ImageContentItem(image_url=ImageUrl(url=_encode(image_path))).
    # TODO 2: return {"answer": response.choices[0].message.content}.
    raise NotImplementedError
