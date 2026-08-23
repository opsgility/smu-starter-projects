"""Smoke test — one FoundryChatClient round-trip. Exits 0/1."""
from __future__ import annotations
import asyncio
import os
import sys

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


async def main() -> int:
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
        client = FoundryChatClient(
            project_endpoint=endpoint,
            model_deployment_name=model,
            credential=DefaultAzureCredential(),
        )
        agent = Agent(chat_client=client, name="VerifyEnvBot", instructions="Reply with the single word 'ok'.")
        response = await agent.run("Reply.")
        text = (response.text or "").strip().lower()
        print(f"[verify_env] agent response = {text!r}")
        return 0 if "ok" in text else 1
    except Exception as exc:  # noqa: BLE001
        print(f"[verify_env] FAILED — {type(exc).__name__}: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
