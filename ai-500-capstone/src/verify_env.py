"""Smoke test - confirm .env, az login, and Foundry reachability before you start the exercises."""
import os
import sys

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


def main() -> int:
    load_dotenv()
    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "")
    model = os.getenv("FOUNDRY_MODEL", "")

    if not endpoint or endpoint.startswith("<") or not model or model.startswith("<"):
        print("ERROR: .env is missing FOUNDRY_PROJECT_ENDPOINT or FOUNDRY_MODEL.")
        print("       Copy the values from the lab's Environment tab into .env, then re-run.")
        return 1

    print(f"Endpoint: {endpoint}")
    print(f"Model:    {model}")

    try:
        project = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
        client = project.get_openai_client()
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with the single word: ready"}],
            max_completion_tokens=32,
        )
        reply = (resp.choices[0].message.content or "").strip()
        print(f"Foundry reply: {reply}")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR calling Foundry: {exc}")
        print("Confirm `az login --use-device-code` completed and the credential holds Foundry User.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
