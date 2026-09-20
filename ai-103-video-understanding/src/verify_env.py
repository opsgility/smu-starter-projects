"""Environment smoke test for the Summitline Video Understanding lab.

Confirms four things before you touch any exercise script:
  1. Every AZURE_* env var expected by the lab is present in .env.
  2. `DefaultAzureCredential` can mint a Cognitive Services token (proves
     `az login --use-device-code` cached a working token).
  3. The Foundry chat deployment (`MODEL_DEPLOYMENT`) exists and responds.
  4. The AI Search endpoint is reachable and the AAD auth path works.

Run with:
    python src/verify_env.py

Exits 0 if everything works, non-zero with a helpful message otherwise.
"""
from __future__ import annotations

import os
import sys
from typing import List

from dotenv import load_dotenv


REQUIRED_VARS: List[str] = [
    "AZURE_AI_PROJECT_ENDPOINT",
    "AZURE_AI_PROJECT_NAME",
    "AZURE_CU_ENDPOINT",
    "MODEL_DEPLOYMENT",
    "EMBEDDING_DEPLOYMENT",
    "AZURE_STORAGE_ACCOUNT_NAME",
    "AZURE_SEARCH_ENDPOINT",
    "AZURE_SEARCH_INDEX_NAME",
]


def _fail(msg: str) -> None:
    print(f"[FAIL] {msg}", file=sys.stderr)
    sys.exit(1)


def _ok(msg: str) -> None:
    print(f"[OK]   {msg}")


def check_env_vars() -> None:
    load_dotenv()
    missing = [v for v in REQUIRED_VARS if not os.environ.get(v)]
    if missing:
        _fail(f"Missing env var(s) in .env: {', '.join(missing)}. "
              "Re-run the ARM-outputs block from Exercise 1 Step 4.")
    placeholders = [v for v in REQUIRED_VARS if "<" in os.environ.get(v, "")]
    if placeholders:
        _fail(f"Env var(s) still hold <placeholder> values: {', '.join(placeholders)}. "
              "Fill them from ARM outputs.")
    _ok(f"All {len(REQUIRED_VARS)} env vars present.")


def check_credential() -> None:
    from azure.identity import DefaultAzureCredential
    try:
        token = DefaultAzureCredential().get_token("https://cognitiveservices.azure.com/.default")
    except Exception as exc:  # noqa: BLE001
        _fail(f"DefaultAzureCredential could not mint a Cognitive Services token: {exc}. "
              "Run `az login --use-device-code` and try again.")
    if not token or not token.token:
        _fail("Token endpoint returned nothing. Re-authenticate with az login.")
    _ok("DefaultAzureCredential minted a Cognitive Services token.")


def check_chat_model() -> None:
    """One-shot round-trip against the gpt chat deployment."""
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    from openai import AzureOpenAI

    # AZURE_AI_PROJECT_ENDPOINT looks like https://<acct>.services.ai.azure.com/api/projects/<name>
    # Strip the /api/projects/... suffix to get the plain Azure OpenAI endpoint.
    project = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    base = project.split("/api/projects/")[0]

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )
    client = AzureOpenAI(
        api_version="2024-10-21",
        azure_endpoint=base,
        azure_ad_token_provider=token_provider,
    )
    try:
        resp = client.chat.completions.create(
            model=os.environ["MODEL_DEPLOYMENT"],
            messages=[{"role": "user", "content": "reply with the single word 'ok'"}],
            max_completion_tokens=8,
        )
    except Exception as exc:  # noqa: BLE001
        _fail(f"Chat round-trip against {os.environ['MODEL_DEPLOYMENT']} failed: {exc}")
    text = (resp.choices[0].message.content or "").strip().lower()
    _ok(f"gpt round-trip returned: '{text}'.")


def check_search() -> None:
    from azure.identity import DefaultAzureCredential
    from azure.search.documents.indexes import SearchIndexClient

    client = SearchIndexClient(
        endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
        credential=DefaultAzureCredential(),
    )
    try:
        # list_index_names is a lightweight probe that also proves RBAC works
        names = list(client.list_index_names())
    except Exception as exc:  # noqa: BLE001
        _fail(f"AI Search AAD probe failed: {exc}. Search Service Contributor "
              "role may not have propagated yet - wait 3 min and retry.")
    _ok(f"AI Search reachable via AAD - {len(names)} existing index(es).")


def main() -> None:
    print("== Summitline Video Understanding - env check ==")
    check_env_vars()
    check_credential()
    check_chat_model()
    check_search()
    print("\n[OK] Environment is ready. Continue to Exercise 2.")


if __name__ == "__main__":
    main()
