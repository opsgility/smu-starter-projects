"""Captions + visual Q&A via a multimodal chat model."""
import base64
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ["CHAT_DEPLOYMENT"]


def _data_url(image_bytes: bytes) -> str:
    return "data:image/png;base64," + base64.b64encode(image_bytes).decode("ascii")


def caption(image_bytes: bytes, *, accessibility: bool = False) -> str:
    instr = (
        "Write a caption suitable as accessibility alt-text. Be concise (under 140 characters), "
        "describe what is visible, do not editorialize."
    ) if accessibility else "Write a one-paragraph caption describing this image."

    with AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential()) as project:
        with project.get_openai_client() as client:
            # TODO 1: Call client.responses.create(model=DEPLOYMENT, input=[
            #             {"role": "user", "content": [
            #                 {"type": "input_text", "text": instr},
            #                 {"type": "input_image", "image_url": _data_url(image_bytes)},
            #             ]}
            #         ]). Return response.output_text.
            raise NotImplementedError


def answer(image_bytes: bytes, question: str) -> str:
    with AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential()) as project:
        with project.get_openai_client() as client:
            # TODO 2: Same shape as caption() but use the user's question as the input_text.
            raise NotImplementedError
