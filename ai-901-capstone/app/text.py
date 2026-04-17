"""Analyze sentiment + entities + key phrases for the /analyze-text endpoint."""
import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["LANGUAGE_ENDPOINT"]
KEY = os.environ["LANGUAGE_KEY"]


def _client() -> TextAnalyticsClient:
    return TextAnalyticsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))


def analyze(content: str) -> dict:
    # TODO 1: run analyze_sentiment, extract_key_phrases, and recognize_entities on [content].
    # TODO 2: return {"sentiment": ..., "key_phrases": [...], "entities": [...]}.
    raise NotImplementedError
