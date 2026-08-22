"""Margie's Travel chat CLI — sync scaffold.

Complete the TODOs in Lesson 6 exercises 3 and 4. When you run
`python src/chat-app.py`, the loop should read your input, send it to
your Foundry deployment with the full conversation history, print the
reply, and remember every turn so follow-ups work naturally.

Kill the loop with Ctrl+D or by typing `/quit`.
"""
import os
import sys

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

SYSTEM_PROMPT = (
    "You are Margie, a warm and pragmatic sales assistant at Margie's Travel, "
    "a boutique travel agency. Help the sales team suggest destinations, draft "
    "itineraries, and answer traveler questions. When you are uncertain, say so "
    "and ask a clarifying question. Keep replies short unless the user asks for detail."
)


def build_client() -> OpenAI:
    """Return an OpenAI client wired to the Foundry project via DefaultAzureCredential."""
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]

    # TODO (Lesson 6 exercise 3): mint a bearer with DefaultAzureCredential and
    # get_bearer_token_provider against the "https://cognitiveservices.azure.com/.default"
    # scope. Construct an OpenAI client with:
    #   - base_url = f"{endpoint}/openai/v1"
    #   - api_key  = <the token from the provider>
    # Return the client. Delete this NotImplementedError once done.
    raise NotImplementedError("Lesson 6 exercise 3: build the OpenAI client here")


def chat_once(client: OpenAI, deployment: str, messages: list[dict]) -> str:
    """Send `messages` to the deployment and return the assistant reply text."""
    # TODO (Lesson 6 exercise 4): call client.chat.completions.create(
    #   model=deployment,
    #   messages=messages,
    #   max_completion_tokens=400,
    # ) and return response.choices[0].message.content.
    # Delete the NotImplementedError once done.
    raise NotImplementedError("Lesson 6 exercise 4: call chat.completions.create here")


def main() -> int:
    load_dotenv()
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    deployment = os.environ.get("MODEL_DEPLOYMENT", "")
    if not endpoint or endpoint.startswith("<") or not deployment or deployment.startswith("<"):
        print("chat-app: fill in AZURE_OPENAI_ENDPOINT and MODEL_DEPLOYMENT in .env first (see verify_env.py)", file=sys.stderr)
        return 1

    client = build_client()
    messages: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Margie's Travel chat — type your message, /quit to exit.")
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
        try:
            reply = chat_once(client, deployment, messages)
        except Exception as e:
            print(f"error: {type(e).__name__}: {e}", file=sys.stderr)
            messages.pop()
            continue

        print(f"Margie> {reply}\n")
        messages.append({"role": "assistant", "content": reply})

    return 0


if __name__ == "__main__":
    sys.exit(main())
