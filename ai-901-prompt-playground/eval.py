"""
Simple eval harness — run each user query against the system prompt via a
Foundry-deployed chat model and print the result for inspection.
"""
import os
from pathlib import Path

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ.get("DEPLOYMENT_NAME", "ai901-chat")
HERE = Path(__file__).parent


def load_prompt() -> str:
    return (HERE / "prompts" / "system_assistant.md").read_text(encoding="utf-8")


def load_queries() -> list[str]:
    text = (HERE / "prompts" / "user_queries.md").read_text(encoding="utf-8")
    return [line.split(". ", 1)[1].strip()
            for line in text.splitlines()
            if line and line[0].isdigit()]


def build_client() -> ChatCompletionsClient:
    # TODO 1: construct a ChatCompletionsClient pointing at ENDPOINT with DefaultAzureCredential().
    #         Use scope="https://cognitiveservices.azure.com/.default" for the token.
    raise NotImplementedError


def run_one(client: ChatCompletionsClient, system_prompt: str, query: str) -> str:
    # TODO 2: call client.complete(model=DEPLOYMENT,
    #                              messages=[SystemMessage(system_prompt), UserMessage(query)])
    #         Return response.choices[0].message.content.
    raise NotImplementedError


def main() -> None:
    client = build_client()
    system_prompt = load_prompt()
    for query in load_queries():
        print(f"\nQ: {query}")
        print(f"A: {run_one(client, system_prompt, query)}")


if __name__ == "__main__":
    main()
