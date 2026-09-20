"""Shared helpers for the Content Understanding REST scaffold."""
from __future__ import annotations

import os

from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ.get("CONTENT_UNDERSTANDING_ENDPOINT")
API_VERSION = os.environ.get("CONTENT_UNDERSTANDING_API_VERSION", "2024-12-01-preview")
ANALYZER_ID = os.environ.get("ANALYZER_ID", "invoice-analyzer")


def require_endpoint() -> str:
    if not ENDPOINT:
        raise SystemExit("Set CONTENT_UNDERSTANDING_ENDPOINT in .env.")
    return ENDPOINT.rstrip("/")


def bearer() -> str:
    return DefaultAzureCredential().get_token(
        "https://cognitiveservices.azure.com/.default"
    ).token


def analyze_url(kind: str) -> str:
    """kind in {documents, images, audio, videos}."""
    return (
        f"{require_endpoint()}/contentunderstanding/analyzers/{ANALYZER_ID}:analyze"
        f"?api-version={API_VERSION}&kind={kind}"
    )
