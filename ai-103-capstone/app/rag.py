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

        # TODO (Exercise 1 Step 8): open AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=CRED)
        # and inside it open the OpenAI client with project.get_openai_client().

        # TODO (Exercise 1 Step 8): embed the question using
        # client.embeddings.create(model=EMBEDDING, input=[question]).data[0].embedding.

        # TODO (Exercise 1 Step 8): call SearchClient(SEARCH_ENDPOINT, INDEX, CRED).search(...)
        # passing search_text=question and vector_queries=[VectorizedQuery(
        #   vector=vec, k_nearest_neighbors=5, fields="embedding")].
        # Select ["source", "markdown"] and top=5.

        # TODO (Exercise 1 Step 8): join the hits into a context string like
        # "[{source}] {markdown}" separated by blank lines.

        # TODO (Exercise 1 Step 8): call client.responses.create(model=DEPLOYMENT, input=[system, user])
        # where system forces citation-only answers and user supplies "Context:\n{ctx}\n\nQ: {question}".
        # Return {"answer": response.output_text, "sources": [r["source"] for r in hits]}.
        raise NotImplementedError(
            "Complete TODOs in app/rag.py (Exercise 1 Step 8)."
        )
