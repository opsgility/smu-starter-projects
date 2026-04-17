"""
Generate an image from a text prompt using DALL-E 3 on Azure OpenAI (deployed
inside your Foundry resource).
"""
import os
import sys
from pathlib import Path

import requests
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
KEY = os.environ["AZURE_OPENAI_API_KEY"]
DEPLOYMENT = os.environ.get("IMAGE_GEN_DEPLOYMENT", "dall-e-3")


def generate(prompt: str, out_path: Path) -> None:
    client = AzureOpenAI(
        azure_endpoint=ENDPOINT,
        api_key=KEY,
        api_version="2024-10-21",
    )

    # TODO 1: call client.images.generate(model=DEPLOYMENT, prompt=prompt, size="1024x1024", n=1).
    # TODO 2: get the returned image url, download with requests, write bytes to out_path.
    raise NotImplementedError


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or "A cozy storefront for Northwind Horizon during autumn"
    generate(prompt, Path("generated.png"))
    print("Wrote generated.png")
