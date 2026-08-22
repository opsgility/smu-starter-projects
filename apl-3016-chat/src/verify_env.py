"""Smoke test: prove .env + DefaultAzureCredential + the deployment all reach.

Exits 0 on a green round-trip, 1 on any failure. Refuses to run against the
placeholder values that ship in .env.example.
"""
import os
import sys

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI


def main() -> int:
    load_dotenv()
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    deployment = os.environ.get("MODEL_DEPLOYMENT", "")

    if not endpoint or not deployment:
        print("verify_env: AZURE_OPENAI_ENDPOINT and MODEL_DEPLOYMENT must both be set in .env", file=sys.stderr)
        return 1
    if endpoint.startswith("<") or deployment.startswith("<"):
        print("verify_env: .env still has placeholder <...> values — fill them in from the lab", file=sys.stderr)
        return 1

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )

    try:
        client = OpenAI(
            base_url=f"{endpoint}/openai/v1",
            api_key=token_provider(),
        )
        reply = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": "Say hello from Margie's Travel."}],
            max_completion_tokens=32,
        )
        print(reply.choices[0].message.content or "(empty reply)")
        return 0
    except Exception as e:
        print(f"verify_env: FAILED — {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
