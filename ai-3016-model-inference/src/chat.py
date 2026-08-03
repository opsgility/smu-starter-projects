"""AI-3016 Lesson 6 — call the deployed GPT-4o model from Python.

Two examples:
  1. Synchronous completion — request, wait, get the full response.
  2. Streaming completion — receive tokens as they are generated.

Both use DefaultAzureCredential (Managed Identity in the lab, Azure CLI on
your dev machine). No hard-coded keys.
"""

import os
from dotenv import load_dotenv

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    SystemMessage,
    UserMessage,
)
from azure.identity import DefaultAzureCredential, get_bearer_token_provider


def make_client() -> ChatCompletionsClient:
    """Build a ChatCompletionsClient using the deployment endpoint + Managed Identity."""
    endpoint = os.environ["AZURE_INFERENCE_ENDPOINT"]
    api_version = os.environ.get("AZURE_INFERENCE_API_VERSION", "2024-08-01-preview")

    # DefaultAzureCredential works across environments:
    #   - Managed Identity when running inside Azure (lab environment)
    #   - Azure CLI (`az login`) when running on your dev machine
    #   - Environment variables when running in CI/CD
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    )

    return ChatCompletionsClient(
        endpoint=endpoint,
        credential=credential,
        api_version=api_version,
    )


def sync_example(client: ChatCompletionsClient) -> None:
    print("\n=== Synchronous completion ===")
    response = client.complete(
        messages=[
            SystemMessage(content="You are Aurora Insights' consulting knowledge copilot. Be concise."),
            UserMessage(content="What are three benefits of cloud computing for consulting firms?"),
        ],
        max_tokens=300,
        temperature=0.3,
    )
    print(response.choices[0].message.content)
    usage = response.usage
    print(f"\n[tokens: {usage.prompt_tokens} in, {usage.completion_tokens} out, {usage.total_tokens} total]")


def streaming_example(client: ChatCompletionsClient) -> None:
    print("\n=== Streaming completion ===")
    stream = client.complete(
        stream=True,
        messages=[
            SystemMessage(content="You are Aurora Insights' consulting knowledge copilot. Be concise."),
            UserMessage(content="What are three benefits of cloud computing for consulting firms?"),
        ],
        max_tokens=300,
        temperature=0.3,
    )
    for update in stream:
        if update.choices and update.choices[0].delta.content:
            print(update.choices[0].delta.content, end="", flush=True)
    print()  # trailing newline


if __name__ == "__main__":
    load_dotenv()
    client = make_client()
    sync_example(client)
    streaming_example(client)
