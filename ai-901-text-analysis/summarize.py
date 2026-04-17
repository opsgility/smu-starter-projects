"""
Use a Foundry-deployed chat model to produce a one-sentence summary.
"""
import os

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
DEPLOYMENT = os.environ.get("DEPLOYMENT_NAME", "ai901-chat")


def summarize_one(review: str) -> str:
    # TODO 1: build a ChatCompletionsClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())
    # TODO 2: call client.complete(
    #             model=DEPLOYMENT,
    #             messages=[
    #                 SystemMessage("Summarize product reviews in one short sentence."),
    #                 UserMessage(review)
    #             ]
    #         )
    # TODO 3: return response.choices[0].message.content.strip()
    raise NotImplementedError
