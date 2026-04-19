"""Foundry client helpers — shared by every route."""
from __future__ import annotations

import os
from functools import lru_cache

from azure.ai.inference import ChatCompletionsClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

FOUNDRY_ENDPOINT = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
DEPLOYMENT = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")


@lru_cache(maxsize=1)
def chat_client() -> ChatCompletionsClient:
    if not FOUNDRY_ENDPOINT:
        raise RuntimeError("Set FOUNDRY_PROJECT_ENDPOINT in .env.")
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    return ChatCompletionsClient(endpoint=FOUNDRY_ENDPOINT, credential=token_provider)
