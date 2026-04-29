"""Exercise 1 — Text-to-image with gpt-image-1 via the Foundry project client."""
import base64
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ["IMAGE_DEPLOYMENT"]


def generate(prompt: str, size: str = "1024x1024") -> bytes:
    """Return PNG bytes for the generated image.

    Call client.images.generate with response_format='b64_json', then
    base64-decode response.data[0].b64_json and return the raw PNG bytes.
    Supported sizes for gpt-image-1: 1024x1024, 1024x1536, 1536x1024.
    """
    # Exercise 1 - Step 7 Start
    raise NotImplementedError("Complete Exercise 1 Step 7")
    # Exercise 1 - Step 7 End
