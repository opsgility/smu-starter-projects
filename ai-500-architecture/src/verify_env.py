"""Smoke test: reach the Foundry project with keyless auth and one chat completion.

Run this FIRST after copying .env.example -> .env and filling in the values.
Exit 0 on success, non-zero on any failure. If this fails, do not touch the
agent stubs — fix .env and role assignments first.
"""
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

    if not endpoint or "<" in endpoint or not model or "<" in model:
        print(
            "ERROR: fill in FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_MODEL in .env first "
            "(angle-bracket placeholders detected).",
            file=sys.stderr,
        )
        return 1

    project = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
    openai_client = project.get_openai_client(api_version="2025-04-01-preview")
    resp = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Say hello from Ridgevault Financial."}],
        max_completion_tokens=64,
    )
    reply = (resp.choices[0].message.content or "").strip()
    print(f"OK: {model} replied: {reply[:200]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
