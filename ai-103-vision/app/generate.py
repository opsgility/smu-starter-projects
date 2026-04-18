"""Text-to-image generation."""
import base64
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ["IMAGE_DEPLOYMENT"]


def generate(prompt: str, size: str = "1024x1024") -> bytes:
    """Return PNG bytes for the generated image."""
    with AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential()) as project:
        with project.get_openai_client() as client:
            # TODO 1: Call client.images.generate(model=DEPLOYMENT, prompt=prompt, size=size,
            #         n=1, response_format="b64_json").
            # TODO 2: Decode and return base64.b64decode(response.data[0].b64_json).
            raise NotImplementedError
