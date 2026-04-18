"""Capstone vision — multimodal Q&A on an uploaded image."""
import base64
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ["MODEL_DEPLOYMENT"]


def _data_url(image_bytes: bytes) -> str:
    return "data:image/png;base64," + base64.b64encode(image_bytes).decode("ascii")


def ask(image_bytes: bytes, question: str) -> str:
    with AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential()) as project:
        with project.get_openai_client() as client:
            # TODO 1: client.responses.create(model=DEPLOYMENT, input=[{"role":"user","content":[
            #             {"type":"input_text","text":question},
            #             {"type":"input_image","image_url":_data_url(image_bytes)}]}]).
            # TODO 2: return response.output_text.
            raise NotImplementedError
