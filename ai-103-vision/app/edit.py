"""Image editing — inpainting via a mask."""
import base64
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ["IMAGE_DEPLOYMENT"]


def edit(image_bytes: bytes, mask_bytes: bytes, prompt: str) -> bytes:
    """Return the edited PNG bytes."""
    with AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential()) as project:
        with project.get_openai_client() as client:
            # TODO 1: Call client.images.edit(model=DEPLOYMENT, image=image_bytes,
            #         mask=mask_bytes, prompt=prompt, n=1, response_format="b64_json").
            # TODO 2: Return base64.b64decode(response.data[0].b64_json).
            raise NotImplementedError
