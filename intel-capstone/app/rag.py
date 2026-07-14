"""/rag — grounded answer with citations over sib-osint-kb (Exercise 1).

Two-client split for the Foundry project surface:

- The Foundry project endpoint (``AIProjectClient.get_openai_client()``)
  routes chat, responses, and agents. Use it for the ``responses.create``
  call that generates the grounded answer.
- The Foundry project endpoint does NOT currently route embeddings
  requests. Embeddings must go directly to the Azure OpenAI
  (account-scoped) endpoint via the ``AzureOpenAI`` client.

Source: https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/embeddings
"""

from __future__ import annotations

import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from openai import AzureOpenAI
from opentelemetry import trace

PROJECT_ENDPOINT = os.environ.get("AZURE_AI_PROJECT_ENDPOINT", "")
AOAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
DEPLOYMENT = os.environ.get("MODEL_DEPLOYMENT", "gpt-5")
EMBEDDING = os.environ.get("EMBEDDING_DEPLOYMENT", "text-embedding-3-large")

SEARCH_ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT", "")
INDEX = os.environ.get("AZURE_SEARCH_INDEX", "sib-osint-kb")

# Single credential reused by the AzureOpenAI (embeddings) client, the
# AIProjectClient (chat/responses), and the SearchClient.
CRED = DefaultAzureCredential()

tracer = trace.get_tracer("sib-osint-capstone")


def answer(question: str) -> dict:
    """Hybrid + semantic retrieval, then grounded Responses generation.

    Returns a dict with ``answer`` (assistant text) and ``sources`` (list of
    the ``source`` field from every search hit, in rank order).

    Client split:
      * Embed the question via ``AzureOpenAI`` (account-scoped endpoint,
        because the Foundry project endpoint does not route embeddings).
      * Generate the grounded response via
        ``AIProjectClient.get_openai_client().responses.create(...)``
        (project-scoped, which is correct for responses/chat/agents).
    """
    with tracer.start_as_current_span("sib.rag.answer") as span:
        span.set_attribute("question.chars", len(question))

        # Exercise 1 - Step 8 Start
        raise NotImplementedError("Complete Exercise 1 Step 8")
        # Exercise 1 - Step 8 End
