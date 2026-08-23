"""Smoke test — confirms the lab's Foundry + Key Vault environment is reachable.

Reads .env, uses DefaultAzureCredential, makes ONE round-trip to the Foundry
gpt-5 deployment. Exits 0 on success, 1 on any failure.
"""
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv


def _missing(name: str, value: str | None) -> bool:
    if not value or value.startswith("<"):
        print(f"  MISSING  {name}  ({value!r}) — fill it in in .env before running")
        return True
    print(f"  OK       {name}")
    return False


def main() -> int:
    load_dotenv()
    print("Ridgevault Zero Trust lab — environment check")
    print("---------------------------------------------")

    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
    model = os.environ.get("FOUNDRY_MODEL")
    kv_name = os.environ.get("KEY_VAULT_NAME")
    kv_uri = os.environ.get("KEY_VAULT_URI")

    issues = 0
    issues += _missing("FOUNDRY_PROJECT_ENDPOINT", endpoint)
    issues += _missing("FOUNDRY_MODEL", model)
    issues += _missing("KEY_VAULT_NAME", kv_name)
    issues += _missing("KEY_VAULT_URI", kv_uri)
    if issues:
        return 1

    try:
        from azure.identity import DefaultAzureCredential
        from openai import AzureOpenAI

        cred = DefaultAzureCredential()

        def _token() -> str:
            return cred.get_token("https://cognitiveservices.azure.com/.default").token

        # The Foundry project endpoint routes v1/openai — strip the projects segment for AOAI-compatible client.
        aoai_base = endpoint.split("/api/projects/")[0]
        client = AzureOpenAI(
            azure_endpoint=aoai_base,
            api_version="2024-08-01-preview",
            azure_ad_token_provider=lambda: _token(),
        )
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Reply with the single word: pong"}],
        )
        reply = (completion.choices[0].message.content or "").strip().lower()
        print(f"\n  Foundry round-trip reply: {reply!r}")
        if "pong" not in reply:
            print("  WARN: unexpected reply, but auth succeeded")
        print("\nEnvironment OK. Proceed to Exercise 2.")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"\n  Foundry round-trip FAILED: {exc}")
        print("\n  Common causes:")
        print("    1. You did not run 'az login --use-device-code' in this terminal.")
        print("    2. The FOUNDRY_PROJECT_ENDPOINT is missing '/api/projects/portfolio-review'.")
        print("    3. Deployment name in FOUNDRY_MODEL differs from what the ARM template output.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
