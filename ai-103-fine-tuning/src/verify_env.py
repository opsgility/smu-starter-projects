"""Smoke test for the fine-tuning starter environment.

Verifies that:
  1. `.env` is present and every required key is filled in (no placeholder values).
  2. `az login --use-device-code` has cached a token that `DefaultAzureCredential`
     can pick up.
  3. The BASE_MODEL_DEPLOYMENT on AZURE_OPENAI_ENDPOINT actually answers a chat
     completion request keylessly.

Run:
    python src/verify_env.py

Exit code:
    0  Environment OK — proceed to Exercise 2.
    1  Something is missing or broken. The error line names the problem.

Mapped to Exercise 1 Step 5.
"""
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv


REQUIRED_KEYS = [
    "AZURE_OPENAI_ENDPOINT",
    "BASE_MODEL_DEPLOYMENT",
    "AZURE_AI_PROJECT_ENDPOINT",
    "AZURE_AI_PROJECT_NAME",
    "AZURE_STORAGE_ACCOUNT_NAME",
    "FINETUNE_JOB_NAME_PREFIX",
]


def _check_env() -> None:
    load_dotenv()
    missing = [k for k in REQUIRED_KEYS if not os.environ.get(k)]
    placeholders = [k for k in REQUIRED_KEYS if (os.environ.get(k) or "").startswith("<")]
    if missing:
        raise RuntimeError(f"Missing .env keys: {', '.join(missing)}")
    if placeholders:
        raise RuntimeError(
            f"Placeholder values still in .env — replace {', '.join(placeholders)} "
            f"with the ARM output values (README step 2)."
        )


def _ping_base_model() -> str:
    """Send one tiny chat request to the base deployment and return the reply text."""
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    from openai import AzureOpenAI

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )
    client = AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
        api_version="2024-10-21",
    )
    resp = client.chat.completions.create(
        model=os.environ["BASE_MODEL_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "Reply with exactly the word: ok"},
            {"role": "user", "content": "verify"},
        ],
        max_completion_tokens=4,
    )
    return (resp.choices[0].message.content or "").strip()


def main() -> int:
    try:
        _check_env()
        reply = _ping_base_model()
        print(f"Base model reply: {reply!r}")
        print("Environment OK — proceed to Exercise 2.")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        print("Fix the above, then re-run: python src/verify_env.py", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
