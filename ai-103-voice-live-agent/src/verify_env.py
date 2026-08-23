"""Exercise 1 — sanity-check the environment.

Prints which env vars are set (values not echoed) and does a fast Azure
identity check so a bad `az login` fails here, not four exercises deeper.
"""
from __future__ import annotations

import os
import sys

from azure.identity import DefaultAzureCredential

REQUIRED = [
    "AZURE_AI_PROJECT_ENDPOINT",
    "AZURE_AI_PROJECT_NAME",
    "AZURE_SPEECH_ENDPOINT",
    "AZURE_SEARCH_ENDPOINT",
    "AZURE_SEARCH_INDEX_NAME",
    "MODEL_DEPLOYMENT",
    "EMBEDDING_DEPLOYMENT",
    "VOICE_LIVE_VOICE",
]


def main() -> int:
    missing = [k for k in REQUIRED if not os.environ.get(k)]
    for k in REQUIRED:
        v = os.environ.get(k, "")
        marker = "OK " if v else "MISS"
        # Show only host for endpoints; hide anything token-shaped.
        shown = ""
        if v.startswith("https://"):
            shown = v.split("/")[2]
        elif not v:
            shown = "<missing>"
        else:
            shown = v
        print(f"  [{marker}] {k:<32} {shown}")

    if missing:
        print(f"\nMissing {len(missing)} env vars. Environment is not ready.")
        return 1

    print("\nEnv OK. Testing Azure identity...")
    cred = DefaultAzureCredential()
    try:
        # ai.azure.com is the correct audience for Voice Live and Foundry.
        token = cred.get_token("https://ai.azure.com/.default")
    except Exception as e:  # noqa: BLE001
        print(f"  DefaultAzureCredential.get_token FAILED: {e}")
        print("  Run:  az login --use-device-code")
        return 2
    print(f"  Got token (expires in ~{(token.expires_on - _now())} s). Ready.")
    return 0


def _now() -> int:
    import time
    return int(time.time())


if __name__ == "__main__":
    sys.exit(main())
