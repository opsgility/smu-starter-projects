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
    # Exercise 1 - Step 7 Start
    raise NotImplementedError("Complete Exercise 1 Step 7")
    # Exercise 1 - Step 7 End
