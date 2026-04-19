"""Run a single user message against a system-prompt file."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
DEPLOYMENT = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")


def run(prompt_path: str, user_message: str, temperature: float = 0.3) -> str:
    if not ENDPOINT:
        raise RuntimeError("Set FOUNDRY_PROJECT_ENDPOINT in .env.")
    system = Path(prompt_path).read_text(encoding="utf-8").strip()
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = ChatCompletionsClient(endpoint=ENDPOINT, credential=token_provider)
    resp = client.complete(
        model=DEPLOYMENT,
        messages=[SystemMessage(system), UserMessage(user_message)],
        temperature=temperature,
    )
    return resp.choices[0].message.content


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True, help="Path to system prompt file")
    parser.add_argument("--message", required=True, help="User message")
    parser.add_argument("--temperature", type=float, default=0.3)
    args = parser.parse_args()
    print(run(args.prompt, args.message, args.temperature))


if __name__ == "__main__":
    main()
