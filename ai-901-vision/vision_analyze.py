"""
Multimodal vision input — send a local image + text prompt to a Foundry
multimodal model and print the model's answer.
"""
import base64
import os
import sys
from pathlib import Path

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import (
    ImageContentItem,
    ImageUrl,
    SystemMessage,
    TextContentItem,
    UserMessage,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ.get("MULTIMODAL_DEPLOYMENT", "gpt-4o")
HERE = Path(__file__).parent


def encode_image(path: Path) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def describe(image_path: Path, question: str) -> str:
    # TODO 1: build a ChatCompletionsClient(endpoint=ENDPOINT, credential=DefaultAzureCredential()).
    # TODO 2: build a UserMessage with content = [
    #             TextContentItem(text=question),
    #             ImageContentItem(image_url=ImageUrl(url=encode_image(image_path)))
    #         ]
    # TODO 3: call client.complete(model=DEPLOYMENT, messages=[SystemMessage("You are a vision assistant."), user_msg])
    # TODO 4: return response.choices[0].message.content
    raise NotImplementedError


if __name__ == "__main__":
    img = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "sample_data" / "storefront.jpg"
    print(describe(img, "Describe this Northwind storefront in two sentences."))
