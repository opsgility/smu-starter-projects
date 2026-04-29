"""/rag — grounded answer with citations over summitline-kb (Exercise 1)."""

from __future__ import annotations

import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from opentelemetry import trace

PROJECT_ENDPOINT = os.environ.get("AZURE_AI_PROJECT_ENDPOINT", "")
DEPLOYMENT = os.environ.get("MODEL_DEPLOYMENT", "gpt-4.1")
EMBEDDING = os.environ.get("EMBEDDING_DEPLOYMENT", "text-embedding-3-large")

SEARCH_ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT", "")
INDEX = os.environ.get("AZURE_SEARCH_INDEX", "summitline-kb")

# Single credential reused by the project client AND the search client.
CRED = DefaultAzureCredential()

tracer = trace.get_tracer("summitline-capstone")


def answer(question: str) -> dict:
    """Hybrid + semantic retrieval, then grounded Responses generation.

    Returns a dict with ``answer`` (assistant text) and ``sources`` (list of
    the ``source`` field from every search hit, in rank order).
    """
    with tracer.start_as_current_span("summitline.rag.answer") as span:
        span.set_attribute("question.chars", len(question))

        # Exercise 1 - Step 8 Start
        raise NotImplementedError("Complete Exercise 1 Step 8")
        # Exercise 1 - Step 8 End
