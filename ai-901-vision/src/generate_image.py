"""Foundry image generation — save the PNG next to the script."""
from __future__ import annotations

import base64
import os
from pathlib import Path

import requests
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ.get("FOUNDRY_PROJECT_ENDPOINT")
DEPLOYMENT = os.environ.get("IMAGE_GEN_DEPLOYMENT_NAME", "dall-e-3")
PROMPT = "A vibrant, modern banner for the 'Northwind Horizon' summer camping sale — tent, lantern, mountain backdrop, warm sunset palette."
OUT = Path(__file__).parent / "generated_banner.png"


def main() -> None:
    if not ENDPOINT:
        raise SystemExit("Set FOUNDRY_PROJECT_ENDPOINT in .env.")
    token = DefaultAzureCredential().get_token("https://cognitiveservices.azure.com/.default").token
    # Foundry image-gen REST endpoint shape — exercise walks through it step by step.
    url = f"{ENDPOINT.rstrip('/')}/deployments/{DEPLOYMENT}/images/generations?api-version=2024-10-21"
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"prompt": PROMPT, "n": 1, "size": "1024x1024", "response_format": "b64_json"},
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    b64 = data["data"][0]["b64_json"]
    OUT.write_bytes(base64.b64decode(b64))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
