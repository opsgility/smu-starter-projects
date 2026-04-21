"""Exercise 2 — Multimodal chat captioning and visual Q&A via the Responses API."""
import base64
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ["CHAT_DEPLOYMENT"]


def _data_url(image_bytes: bytes) -> str:
    """Encode raw PNG bytes as a data: URL for the Responses API input_image part."""
    b64 = base64.b64encode(image_bytes).decode("ascii")
    return f"data:image/png;base64,{b64}"


def caption(image_bytes: bytes, *, accessibility: bool = False) -> str:
    """Return a caption for the image.

    When accessibility=True, produce alt-text style output:
      - under 140 characters
      - describe only what is visible
      - no editorializing

    Otherwise produce a one-paragraph descriptive caption.

    Use the Responses API with a user message whose content is a list of
    two content parts: an 'input_text' with the instruction and an
    'input_image' with the image as a data: URL (use _data_url()).
    Return response.output_text.
    """
    # TODO (Exercise 2 Step 2): Build the instruction string based on the
    #   accessibility flag, then call client.responses.create on
    #   AIProjectClient.get_openai_client() with a user message containing
    #   input_text + input_image content parts. Return response.output_text.
    raise NotImplementedError("Implement caption() in Exercise 2 Step 2")


def answer(image_bytes: bytes, question: str) -> str:
    """Answer a free-form question about the image.

    Same Responses API shape as caption(): a user message with an input_text
    (the question) and an input_image (the data: URL). Return response.output_text.
    """
    # TODO (Exercise 2 Step 3): Call client.responses.create with the question
    #   as input_text and the image as input_image; return response.output_text.
    raise NotImplementedError("Implement answer() in Exercise 2 Step 3")
