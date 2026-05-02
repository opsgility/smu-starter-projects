"""Text analysis and structured extraction helpers for Summitline Outfitters.

Exercise 1 wires two complementary NLP patterns into the FastAPI service:

- ``analyze(content)``    — fixed-shape NLP from the Azure AI **Language** service
                            (sentiment + confidence scores + key phrases).
- ``extract(content)``    — schema-driven JSON extraction via the Azure OpenAI
                            **Responses API** against a ``gpt-4.1`` deployment
                            in an Azure AI Foundry project.

Both helpers are called from ``app/main.py``; students only fill in the
``TODO`` markers below.
"""

from __future__ import annotations

import json
import os

from azure.ai.projects import AIProjectClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Environment wiring (populated from ARM template outputs in Exercise 1).
# ---------------------------------------------------------------------------
PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
MODEL = os.environ["MODEL_DEPLOYMENT"]
LANGUAGE_ENDPOINT = os.environ["LANGUAGE_ENDPOINT"]
LANGUAGE_KEY = os.environ["LANGUAGE_KEY"]

# System prompt that steers the Responses API toward a predictable JSON shape.
EXTRACTION_PROMPT = (
    "You extract structured data from free-form trip reports for "
    "Summitline Outfitters. Return ONLY a JSON object (no prose, no Markdown "
    "fences) with exactly these keys:\n"
    '  "people":        array of person names mentioned,\n'
    '  "organizations": array of companies / teams mentioned,\n'
    '  "products":      array of Summitline product names mentioned,\n'
    '  "summary":       one-sentence summary of the report.\n'
    "If a category has no values, return an empty array."
)

# Shared Text Analytics client — safe to reuse across requests.
_lang = TextAnalyticsClient(
    endpoint=LANGUAGE_ENDPOINT,
    credential=AzureKeyCredential(LANGUAGE_KEY),
)


def analyze(content: str) -> dict:
    """Combined sentiment + key phrases via the Azure AI Language service.

    Returns a flat dict so FastAPI can serialize it directly:

        {
            "sentiment":   "positive" | "neutral" | "negative" | "mixed",
            "confidence":  {"positive": 0.98, "neutral": 0.01, "negative": 0.01},
            "key_phrases": ["Aurora parka", "minus twenty", ...],
        }
    """
    # Exercise 1 - Step 9 Start
    raise NotImplementedError("Complete Exercise 1 Step 9")
    # Exercise 1 - Step 9 End


def extract(content: str) -> dict:
    """Structured extraction using the Azure OpenAI Responses API.

    Uses ``AIProjectClient.get_openai_client()`` so the call is routed through
    the Foundry project and auth flows through ``DefaultAzureCredential``
    (Azure CLI token in the lab VM).
    """
    # Exercise 1 - Step 10 Start
    raise NotImplementedError("Complete Exercise 1 Step 10")
    # Exercise 1 - Step 10 End
