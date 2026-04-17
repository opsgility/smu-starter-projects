"""
AI-901 Lesson 1 — Responsible AI with Azure AI Content Safety

You'll complete the TODOs below to evaluate sample texts against the
six Responsible AI principles: fairness, reliability/safety, privacy/security,
inclusiveness, transparency, accountability.
"""
import json
import os
from pathlib import Path

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["CONTENT_SAFETY_ENDPOINT"]
KEY = os.environ["CONTENT_SAFETY_KEY"]


def get_client() -> ContentSafetyClient:
    # TODO 1: return a ContentSafetyClient authenticated with AzureKeyCredential(KEY).
    raise NotImplementedError


def analyze_text(client: ContentSafetyClient, text: str) -> dict:
    """Return a dict with severity scores for Hate, Violence, Sexual, SelfHarm."""
    # TODO 2: build an AnalyzeTextOptions request for the four TextCategory values.
    #         Call client.analyze_text(...) and return a dict mapping category name -> severity.
    raise NotImplementedError


def load_samples() -> list[dict]:
    path = Path(__file__).parent / "sample_data" / "texts.json"
    return json.loads(path.read_text(encoding="utf-8"))


def score_against_rubric(text: str, scores: dict) -> str:
    """Return a short verdict using the RAI rubric in rubric.md."""
    # TODO 3: if any severity >= 2, return "blocked — <category>"; else "allowed".
    raise NotImplementedError


def main() -> None:
    client = get_client()
    for sample in load_samples():
        scores = analyze_text(client, sample["text"])
        verdict = score_against_rubric(sample["text"], scores)
        print(f"[{sample['principle']}] {verdict} :: {scores}")


if __name__ == "__main__":
    main()
