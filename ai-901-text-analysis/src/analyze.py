"""Azure AI Language scaffold — four stubs, students implement."""
from __future__ import annotations

import os
from pathlib import Path

from azure.ai.textanalytics import TextAnalyticsClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ.get("LANGUAGE_ENDPOINT")
SAMPLE = Path(__file__).parent.parent / "sample_data" / "reviews.txt"


def build_client() -> TextAnalyticsClient:
    if not ENDPOINT:
        raise RuntimeError("Set LANGUAGE_ENDPOINT in .env.")
    return TextAnalyticsClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())


def extract_key_phrases(client: TextAnalyticsClient, text: str) -> list[str]:
    """TODO: call client.extract_key_phrases([text]) and return the phrases list."""
    raise NotImplementedError


def recognize_entities(client: TextAnalyticsClient, text: str) -> list[dict]:
    """TODO: call client.recognize_entities([text]) and return [{text, category}, ...]."""
    raise NotImplementedError


def analyze_sentiment(client: TextAnalyticsClient, text: str) -> dict:
    """TODO: call client.analyze_sentiment([text]) and return {sentiment, scores}."""
    raise NotImplementedError


def summarize_text(client: TextAnalyticsClient, text: str) -> str:
    """TODO: call client.begin_extract_summary and return the joined summary sentences."""
    raise NotImplementedError


def main() -> None:
    client = build_client()
    for line in SAMPLE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        print(f"\n--- {line[:80]}")
        for fn in (extract_key_phrases, recognize_entities, analyze_sentiment, summarize_text):
            try:
                print(f"  {fn.__name__}: {fn(client, line)}")
            except NotImplementedError:
                print(f"  {fn.__name__}: (TODO — implement in exercise)")


if __name__ == "__main__":
    main()
