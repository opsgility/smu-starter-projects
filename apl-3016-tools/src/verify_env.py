"""Smoke test: reach Foundry with keyless auth and one chat completion.

Run this FIRST after copying .env.example -> .env and filling in the values.
Exit 0 on success, non-zero on any failure. If this fails, do not touch the
lab code — fix .env and role assignments first.
"""
from __future__ import annotations
import os
import sys

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import OpenAI


def main() -> int:
    load_dotenv()
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    deployment = os.environ.get("MODEL_DEPLOYMENT", "")

    if not endpoint or "<" in endpoint or not deployment or "<" in deployment:
        print("ERROR: fill in AZURE_OPENAI_ENDPOINT and MODEL_DEPLOYMENT in .env first (angle-bracket placeholders detected).", file=sys.stderr)
        return 1

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = OpenAI(
        base_url=f"{endpoint}/openai/v1",
        default_headers={"Authorization": f"Bearer {token_provider()}"},
        api_key="unused",
    )
    resp = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": "Say hello from Margie's Travel."}],
        max_completion_tokens=64,
    )
    reply = resp.choices[0].message.content or ""
    print(f"OK: {deployment} replied: {reply.strip()[:200]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
