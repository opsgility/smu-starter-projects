"""Classify a free-text scenario into one of the AI-901 workload families."""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
DEPLOYMENT = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")

SYSTEM_PROMPT = """You are an Azure AI architect. Classify the user's scenario into
exactly one of these AI-901 workload families and suggest the primary Azure service:

1. Generative / Agentic AI  — Azure OpenAI / Foundry Agents
2. Text Analysis            — Azure AI Language
3. Speech                   — Azure AI Speech
4. Computer Vision          — Azure AI Vision (+ image generation via Foundry)
5. Information Extraction   — Azure AI Content Understanding

Respond in this exact format:
WORKLOAD: <family>
SERVICE: <azure service>
REASON: <one sentence>
"""


def build_client() -> ChatCompletionsClient:
    if not ENDPOINT:
        raise RuntimeError("Set FOUNDRY_PROJECT_ENDPOINT in .env.")
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    return ChatCompletionsClient(endpoint=ENDPOINT, credential=token_provider)


def classify(client: ChatCompletionsClient, scenario: str) -> str:
    resp = client.complete(
        model=DEPLOYMENT,
        messages=[SystemMessage(SYSTEM_PROMPT), UserMessage(scenario.strip())],
        temperature=0.0,
    )
    return resp.choices[0].message.content


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", help="Single scenario text")
    parser.add_argument("--file", help="Path to a file with one scenario per line")
    args = parser.parse_args()

    client = build_client()

    if args.file:
        for line in Path(args.file).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            print(f"\n--- {line[:80]}")
            print(classify(client, line))
        return

    scenario = args.scenario or sys.stdin.read()
    if not scenario.strip():
        sys.exit("Provide --scenario or --file or pipe text on stdin.")
    print(classify(client, scenario))


if __name__ == "__main__":
    main()
