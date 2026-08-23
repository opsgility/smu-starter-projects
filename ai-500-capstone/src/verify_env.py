"""Smoke test — confirm .env, az login, and Foundry reachability before you start the exercises."""
import os
import sys

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


def main() -> int:
    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "")
    model = os.getenv("FOUNDRY_MODEL", "")

    if not endpoint or endpoint.startswith("<") or not model or model.startswith("<"):
        print("ERROR: .env is missing FOUNDRY_PROJECT_ENDPOINT or FOUNDRY_MODEL.")
        print("       Copy the values from the lab's Environment tab into .env, then re-run.")
        return 1

    print(f"Endpoint: {endpoint}")
    print(f"Model:    {model}")

    try:
        client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
        chat = client.inference.get_chat_completions_client()
        response = chat.complete(
            model=model,
            messages=[{"role": "user", "content": "Reply with the single word: ready"}],
        )
        reply = response.choices[0].message.content.strip()
        print(f"Foundry reply: {reply}")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR calling Foundry: {exc}")
        print("Confirm `az login --use-device-code` completed and the credential holds Foundry User.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
