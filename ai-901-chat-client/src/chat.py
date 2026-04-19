"""Plain single-turn chat REPL — exercise adds system prompt, history, streaming."""
from __future__ import annotations

import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
DEPLOYMENT = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")


def build_client() -> ChatCompletionsClient:
    if not ENDPOINT:
        raise RuntimeError("Set FOUNDRY_PROJECT_ENDPOINT in .env.")
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    return ChatCompletionsClient(endpoint=ENDPOINT, credential=token_provider)


def main() -> None:
    client = build_client()
    print(f"Chat (deployment: {DEPLOYMENT}). Ctrl+C to exit.\n")
    while True:
        try:
            user = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not user:
            continue
        resp = client.complete(
            model=DEPLOYMENT,
            messages=[UserMessage(user)],
            temperature=0.4,
        )
        print(f"bot> {resp.choices[0].message.content}\n")


if __name__ == "__main__":
    main()
