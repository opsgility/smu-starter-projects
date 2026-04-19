"""AI-901 · Responsible AI — Content Safety scaffold.

Loads sample prompts, scores them with Azure AI Content Safety, and prints
category severities. The `run_rai_gate` function is a TODO — the exercise has
you decide which prompts to block, which to flag for review, and which to allow.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ.get("CONTENT_SAFETY_ENDPOINT")
if not ENDPOINT:
    raise RuntimeError("Set CONTENT_SAFETY_ENDPOINT in .env (see .env.example).")

SAMPLE_PROMPTS = Path(__file__).parent.parent / "sample_data" / "prompts.json"


def build_client() -> ContentSafetyClient:
    credential = DefaultAzureCredential()
    return ContentSafetyClient(endpoint=ENDPOINT, credential=credential)


def score_prompt(client: ContentSafetyClient, text: str) -> dict:
    result = client.analyze_text(AnalyzeTextOptions(text=text))
    return {c.category: c.severity for c in result.categories_analysis}


def run_rai_gate(scores: dict) -> str:
    """TODO (exercise): return 'block', 'review', or 'allow' based on severities."""
    raise NotImplementedError("Implement in the exercise — gate on severity thresholds.")


def main() -> None:
    prompts = json.loads(SAMPLE_PROMPTS.read_text(encoding="utf-8"))
    client = build_client()
    print(f"{'id':<4} {'severities (hate/sex/violence/selfharm)':<50} preview")
    print("-" * 100)
    for p in prompts:
        scores = score_prompt(client, p["text"])
        preview = p["text"][:60].replace("\n", " ")
        sev = (
            f"{scores.get('Hate', 0)}/"
            f"{scores.get('Sexual', 0)}/"
            f"{scores.get('Violence', 0)}/"
            f"{scores.get('SelfHarm', 0)}"
        )
        print(f"{p['id']:<4} {sev:<50} {preview}")


if __name__ == "__main__":
    main()
