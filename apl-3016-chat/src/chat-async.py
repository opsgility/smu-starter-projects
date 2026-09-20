"""Async, streaming variant of chat-app.py.

You fill in the TODOs in Lesson 6 exercise 5:
  - Build an AsyncOpenAI client
  - Call chat.completions.create with stream=True
  - Print each chunk as it arrives so the reply appears token-by-token

Run with:
  python src/chat-async.py

Ctrl+C to quit.
"""
from __future__ import annotations
import asyncio
import os
import sys

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import AsyncOpenAI


def system_prompt() -> str:
    return (
        "You are a helpful assistant for Margie's Travel — a boutique travel "
        "agency. Reply in short paragraphs. If asked about cancellations or "
        "policies, quote provided policy text verbatim."
    )


async def build_client() -> AsyncOpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    # TODO (Exercise 5): construct an AsyncOpenAI client — same shape as the
    # sync one in chat-app.py but async. Reuse the DefaultAzureCredential
    # bearer pattern.
    raise NotImplementedError("TODO Exercise 5: construct the AsyncOpenAI client")


async def stream_reply(client: AsyncOpenAI, messages: list[dict], deployment: str) -> str:
    # TODO (Exercise 5): call client.chat.completions.create with stream=True.
    # Iterate the async stream, print each chunk.choices[0].delta.content as it
    # arrives (flush after each write so tokens render live), and return the
    # accumulated reply so main() can append it to `messages`.
    raise NotImplementedError("TODO Exercise 5: iterate the stream and print chunks")


async def main() -> int:
    load_dotenv()
    deployment = os.environ["MODEL_DEPLOYMENT"]
    client = await build_client()
    messages: list[dict] = [{"role": "system", "content": system_prompt()}]

    print(f"Margie chat (async, {deployment}) — Ctrl+C to quit.")
    while True:
        try:
            user = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not user:
            continue
        messages.append({"role": "user", "content": user})
        print("margie> ", end="", flush=True)
        reply = await stream_reply(client, messages, deployment)
        print()
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
