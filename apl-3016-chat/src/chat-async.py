"""Margie's Travel chat CLI — async streaming scaffold.

Complete the TODOs in Lesson 6 exercise 5. When you run
`python src/chat-async.py`, the loop should read your input, stream the
model's reply token-by-token to stdout, and keep the conversation state
across turns.

Kill the loop with Ctrl+D or by typing `/quit`.
"""
import asyncio
import os
import sys

from dotenv import load_dotenv
from azure.identity.aio import DefaultAzureCredential
from azure.identity.aio import get_bearer_token_provider
from openai import AsyncOpenAI

SYSTEM_PROMPT = (
    "You are Margie, a warm and pragmatic sales assistant at Margie's Travel, "
    "a boutique travel agency. Help the sales team suggest destinations, draft "
    "itineraries, and answer traveler questions. When you are uncertain, say so "
    "and ask a clarifying question. Keep replies short unless the user asks for detail."
)


async def build_client(credential: DefaultAzureCredential) -> AsyncOpenAI:
    """Return an AsyncOpenAI client wired to the Foundry project."""
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]

    # TODO (Lesson 6 exercise 5, part A): wrap the async credential in
    # get_bearer_token_provider against "https://cognitiveservices.azure.com/.default",
    # await the provider once to mint a bearer, then construct an AsyncOpenAI
    # client with base_url=f"{endpoint}/openai/v1" and api_key=<the token>.
    # Return the client. Delete this NotImplementedError once done.
    raise NotImplementedError("Lesson 6 exercise 5A: build the AsyncOpenAI client here")


async def stream_reply(client: AsyncOpenAI, deployment: str, messages: list[dict]) -> str:
    """Stream one reply to stdout and return the full text for history."""
    # TODO (Lesson 6 exercise 5, part B): call
    #   stream = await client.chat.completions.create(
    #       model=deployment, messages=messages,
    #       max_completion_tokens=400, stream=True,
    #   )
    # Iterate `async for chunk in stream:` — each chunk.choices[0].delta.content
    # may be None or a token string. Print each token via `print(token, end="", flush=True)`
    # and accumulate into a `full` string. When the stream ends, print a newline
    # and return `full`. Delete the NotImplementedError once done.
    raise NotImplementedError("Lesson 6 exercise 5B: stream tokens from chat.completions here")


async def main() -> int:
    load_dotenv()
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    deployment = os.environ.get("MODEL_DEPLOYMENT", "")
    if not endpoint or endpoint.startswith("<") or not deployment or deployment.startswith("<"):
        print("chat-async: fill in AZURE_OPENAI_ENDPOINT and MODEL_DEPLOYMENT in .env first (see verify_env.py)", file=sys.stderr)
        return 1

    async with DefaultAzureCredential() as credential:
        client = await build_client(credential)
        messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

        print("Margie's Travel chat (streaming) — type your message, /quit to exit.")
        while True:
            try:
                user_input = input("you> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break

            if not user_input:
                continue
            if user_input.lower() in {"/quit", "/exit"}:
                break

            messages.append({"role": "user", "content": user_input})
            print("Margie> ", end="", flush=True)
            try:
                reply = await stream_reply(client, deployment, messages)
            except Exception as e:
                print(f"\nerror: {type(e).__name__}: {e}", file=sys.stderr)
                messages.pop()
                continue

            messages.append({"role": "assistant", "content": reply})

    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
