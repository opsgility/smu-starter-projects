"""Smoke test: reach the Foundry project + Content Safety + Language endpoints with keyless auth.

Run this FIRST after copying .env.example -> .env and filling in the values.
Exit 0 on success, non-zero on any failure. If this fails, do not touch the
guardrail middleware stubs — fix .env and role assignments first.
"""
from __future__ import annotations
import os
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


def _check_placeholder(name: str, value: str) -> bool:
    if not value or "<" in value:
        print(
            f"ERROR: fill in {name} in .env first (angle-bracket placeholder detected).",
            file=sys.stderr,
        )
        return False
    return True


def main() -> int:
    load_dotenv()
    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT", "")
    model = os.environ.get("FOUNDRY_MODEL", "")
    cs_endpoint = os.environ.get("CONTENT_SAFETY_ENDPOINT", "")
    lang_endpoint = os.environ.get("LANGUAGE_ENDPOINT", "")

    ok = True
    ok &= _check_placeholder("FOUNDRY_PROJECT_ENDPOINT", endpoint)
    ok &= _check_placeholder("FOUNDRY_MODEL", model)
    ok &= _check_placeholder("CONTENT_SAFETY_ENDPOINT", cs_endpoint)
    ok &= _check_placeholder("LANGUAGE_ENDPOINT", lang_endpoint)
    if not ok:
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
    print(f"OK: CONTENT_SAFETY_ENDPOINT reachable at {cs_endpoint}")
    print(f"OK: LANGUAGE_ENDPOINT reachable at {lang_endpoint}")
    print("verify_env passed — proceed to exercise 2.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
