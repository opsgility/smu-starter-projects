"""Sync chat REPL against a Foundry-hosted gpt-5.2 deployment.

You fill in the TODOs in Lesson 6 exercises 3 and 4:
  - Exercise 3: build the OpenAI client and call chat.completions.create
  - Exercise 4: keep a rolling `messages` list so the model remembers the turn

Run with:
  python src/chat-app.py

Ctrl+C to quit.
"""
from __future__ import annotations
import os
import sys

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import OpenAI


def build_client() -> OpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    # TODO (Exercise 3): construct an OpenAI client whose base_url points at
    # the Foundry project's OpenAI-compatible v1 surface, using a bearer minted
    # from DefaultAzureCredential. See src/verify_env.py for the exact shape.
    raise NotImplementedError("TODO Exercise 3: construct the OpenAI client")


def system_prompt() -> str:
    return (
        "You are a helpful assistant for Margie's Travel — a boutique travel "
        "agency. Answer briefly, suggest destinations by region + season, and "
        "cite any provided policy text verbatim when asked about cancellations."
    )


def main() -> int:
    load_dotenv()
    deployment = os.environ["MODEL_DEPLOYMENT"]
    client = build_client()

    # TODO (Exercise 4): initialize `messages` with a system prompt so the model
    # keeps the Margie's Travel persona across turns. Append every user turn AND
    # every assistant reply to `messages` before the next call so the model
    # remembers the conversation.
    messages: list[dict] = []

    print(f"Margie chat ({deployment}) — Ctrl+C to quit.")
    while True:
        try:
            user = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not user:
            continue

        # TODO (Exercise 3): call client.chat.completions.create with `messages`
        # as the conversation so far, print the assistant reply, and append the
        # reply back onto `messages` for the next turn.
        raise NotImplementedError("TODO Exercise 3: send the request and print the reply")


if __name__ == "__main__":
    sys.exit(main())
