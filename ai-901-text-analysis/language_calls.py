"""
Thin wrappers around Azure AI Language (TextAnalyticsClient).
"""
import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["LANGUAGE_ENDPOINT"]
KEY = os.environ["LANGUAGE_KEY"]


def _client() -> TextAnalyticsClient:
    return TextAnalyticsClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))


def analyze_sentiment(docs: list[str]) -> list[dict]:
    """Return [{'sentiment': str, 'confidence': dict}] per document."""
    # TODO 1: call _client().analyze_sentiment(docs) and map the response into the return shape.
    raise NotImplementedError


def analyze_key_phrases(docs: list[str]) -> list[list[str]]:
    """Return a list of key-phrase lists, one per document."""
    # TODO 2: call _client().extract_key_phrases(docs) and return result.key_phrases for each doc.
    raise NotImplementedError


def analyze_entities(docs: list[str]) -> list[list[dict]]:
    """Return a list of entity lists (each with {'text', 'category'}) per document."""
    # TODO 3: call _client().recognize_entities(docs) and map each entity to {text, category}.
    raise NotImplementedError
