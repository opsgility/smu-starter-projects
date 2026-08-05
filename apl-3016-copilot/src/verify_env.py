# Smoke test for the Halcyon Assist starter. Reads .env, opens an AIProjectClient
# with DefaultAzureCredential, and sends a single chat completion.
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


REQUIRED_VARS = (
    "AZURE_AI_PROJECT_ENDPOINT",
    "AZURE_AI_CHAT_DEPLOYMENT",
)


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value or value.startswith("<"):
        print(f"[verify_env] Missing env var: set this variable in .env -> {name}")
        sys.exit(1)
    return value


def main() -> None:
    load_dotenv()

    for name in REQUIRED_VARS:
        require_env(name)

    endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    deployment = os.environ["AZURE_AI_CHAT_DEPLOYMENT"]

    credential = DefaultAzureCredential()
    project = AIProjectClient(endpoint=endpoint, credential=credential)

    chat = project.inference.get_chat_completions_client()
    response = chat.complete(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Halcyon Assist, a policy-lookup copilot for Halcyon "
                    "Insurance customer-service agents. Reply in one short sentence."
                ),
            },
            {
                "role": "user",
                "content": "In one sentence, confirm that this Halcyon Assist environment is wired up.",
            },
        ],
    )

    reply = response.choices[0].message.content
    print(f"[verify_env] Model deployment: {deployment}")
    print(f"[verify_env] Reply: {reply}")


if __name__ == "__main__":
    main()
