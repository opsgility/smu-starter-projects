"""Exercise 1 — Mask-based inpainting with gpt-image-1 (images.edit)."""
import base64
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ["IMAGE_DEPLOYMENT"]


def edit(image_bytes: bytes, mask_bytes: bytes, prompt: str) -> bytes:
    """Return the edited PNG bytes.

    Mask alpha-channel convention for gpt-image-1:
      alpha = 0   (transparent) -> REGENERATE this pixel
      alpha = 255 (opaque)      -> PRESERVE the source pixel

    Call client.images.edit with model, image, mask, prompt,
    response_format='b64_json', then base64-decode response.data[0].b64_json.
    """
    # TODO (Exercise 1 Step 8): Call images.edit via AIProjectClient with
    #   DefaultAzureCredential, passing image_bytes and mask_bytes, and
    #   return the base64-decoded PNG bytes from response.data[0].b64_json.
    raise NotImplementedError("Implement edit() in Exercise 1 Step 8")
