"""Smoke test — one AIProjectClient round-trip. Exits 0/1."""
from __future__ import annotations
import os
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


REQUIRED = (
    "FOUNDRY_PROJECT_ENDPOINT",
    "FOUNDRY_MODEL",
    "FUNCTION_APP_NAME",
    "FUNCTION_APP_URL",
    "STORAGE_ACCOUNT_NAME",
)


def main() -> int:
    load_dotenv()

    values = {name: os.environ.get(name, "") for name in REQUIRED}
    for name, value in values.items():
        if not value or "<" in value:
            print(f"[verify_env] {name} missing or placeholder — copy .env.example to .env.")
            return 1
        print(f"[verify_env] {name} = {value}")

    try:
        client = AIProjectClient(
            endpoint=values["FOUNDRY_PROJECT_ENDPOINT"],
            credential=DefaultAzureCredential(),
        )
        agents = list(client.agents.list_agents())
        print(f"[verify_env] Foundry round-trip OK — {len(agents)} agent(s) in project.")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"[verify_env] FAILED — {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
