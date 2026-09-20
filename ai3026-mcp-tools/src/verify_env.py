"""Smoke test — one AIProjectClient round-trip. Exits 0/1."""
from __future__ import annotations
import os
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


def main() -> int:
    load_dotenv()
    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT", "")
    model = os.environ.get("FOUNDRY_MODEL", "")

    for name, value in (("FOUNDRY_PROJECT_ENDPOINT", endpoint), ("FOUNDRY_MODEL", model)):
        if not value or "<" in value:
            print(f"[verify_env] {name} missing or placeholder — copy .env.example to .env and fill in.")
            return 1

    print(f"[verify_env] endpoint = {endpoint}")
    print(f"[verify_env] model    = {model}")

    try:
        client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
        agents = list(client.agents.list_agents())
        print(f"[verify_env] round-trip OK — {len(agents)} agent(s) currently in project")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"[verify_env] FAILED — {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
