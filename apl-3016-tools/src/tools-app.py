"""Responses API + built-in tools (web_search + file_search) for Margie's Travel.

You fill in the TODOs in Lesson 8 exercises 3 and 4:
  - Exercise 3: build the OpenAI client, call responses.create with web_search
  - Exercise 4: upload brochures/*.md to a Foundry vector store, then add
    file_search with vector_store_ids to the tools list

Run with:
  python src/tools-app.py "What's the weather in Copenhagen next week, and what does our Baltic cruise brochure say about excursions there?"
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import OpenAI

BROCHURES_DIR = Path(__file__).resolve().parent.parent / "brochures"
VECTOR_STORE_ID_PATH = Path(__file__).resolve().parent.parent / "vector_store_id.txt"


def build_client() -> OpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    return OpenAI(
        base_url=f"{endpoint}/openai/v1",
        default_headers={"Authorization": f"Bearer {token_provider()}"},
        api_key="unused",
    )


def ensure_vector_store(client: OpenAI) -> str:
    """Cache the vector-store id across runs so the student doesn't re-upload
    brochures every invocation. Delete vector_store_id.txt to rebuild."""
    if VECTOR_STORE_ID_PATH.exists():
        return VECTOR_STORE_ID_PATH.read_text().strip()

    # TODO (Exercise 4): create a vector store, upload every .md file in
    # BROCHURES_DIR to it, wait for indexing to finish, write the vector-store
    # id to VECTOR_STORE_ID_PATH, and return it.
    #
    # See https://learn.microsoft.com/azure/foundry/agents/how-to/tools/file-search
    # for the exact client.vector_stores.* / client.vector_stores.files.* calls.
    raise NotImplementedError("TODO Exercise 4: create the vector store and upload brochures/*.md")


def answer(client: OpenAI, question: str, deployment: str) -> str:
    # TODO (Exercise 3): call client.responses.create with:
    #   - model=deployment
    #   - input=question
    #   - tools=[{"type": "web_search"}]
    # Print the tool_calls trace and return the final response text.
    #
    # TODO (Exercise 4): extend the tools list with a file_search entry that
    # references your vector_store_id (via ensure_vector_store(client)) so the
    # model can cite the brochures.
    raise NotImplementedError("TODO Exercise 3: call responses.create with web_search")


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: python src/tools-app.py '<question>'", file=sys.stderr)
        return 2
    question = sys.argv[1]
    deployment = os.environ["MODEL_DEPLOYMENT"]
    client = build_client()
    reply = answer(client, question, deployment)
    print(reply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
