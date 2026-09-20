"""Azure AI Search retrieval for the Summitline Outfitters RAG pipeline.

Exercises 1 and 2 ask you to fill in `create_index()`, `ingest()`, and
`search()`. The `_chunk()` and `_embed()` helpers are fully implemented for
you — do not modify them.

Run from the project root:

    python -c "from app import retrieval; retrieval.create_index(); print('ok')"
    python -m app.retrieval ingest
    python -m app.retrieval search "What is the Summitline return policy?"
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
    VectorSearch,
    VectorSearchProfile,
)
from azure.search.documents.models import VectorizedQuery

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT", "")
INDEX = os.environ.get("AZURE_SEARCH_INDEX", "summitline-rag")
PROJECT_ENDPOINT = os.environ.get("AZURE_AI_PROJECT_ENDPOINT", "")
EMBEDDING_DEPLOYMENT = os.environ.get("EMBEDDING_DEPLOYMENT", "text-embedding-3-small")

# text-embedding-3-small produces 1536-dim vectors. If you swap in
# text-embedding-3-large, change this to 3072 AND update the index.
EMBED_DIMENSIONS = 1536

CRED = DefaultAzureCredential()

# sample_docs lives next to the app package at the project root.
SAMPLE_DOCS = Path(__file__).resolve().parent.parent / "sample_docs"


# ---------------------------------------------------------------------------
# Exercise 1 — create the AI Search index
# ---------------------------------------------------------------------------

def create_index() -> None:
    """Create (or update) the `summitline-rag` index.

    The schema must define four fields — `id` (key), `source` (filterable
    string), `chunk` (searchable string), and `embedding` (vector collection of
    `EMBED_DIMENSIONS` singles) — plus a `VectorSearch` configuration with an
    HNSW algorithm and a profile named `default`, and a `SemanticSearch`
    configuration with a single `SemanticConfiguration` named `default` whose
    prioritized content field is `chunk`.
    """
    # Exercise 1 - Step 6 Start
    raise NotImplementedError("Complete Exercise 1 Step 6")
    # Exercise 1 - Step 6 End


# ---------------------------------------------------------------------------
# Exercise 2 — ingest and search
# ---------------------------------------------------------------------------

def ingest() -> None:
    """Chunk every Markdown file under `sample_docs/`, embed, and upload.

    For each file: chunk with `_chunk()`, batch-embed the chunks with
    `_embed()`, build `{id, source, chunk, embedding}` dicts, and upload them
    via `SearchClient.upload_documents`.
    """
    # Exercise 2 - Step 1 Start
    raise NotImplementedError("Complete Exercise 2 Step 1")
    # Exercise 2 - Step 1 End


def search(query: str, k: int = 5) -> list[dict]:
    """Hybrid (vector + keyword) + semantic search for the top-k chunks.

    Returns a list of dicts with `id`, `source`, `chunk`, and `score` keys,
    ordered by semantic reranker score.
    """
    # Exercise 2 - Step 2 Start
    raise NotImplementedError("Complete Exercise 2 Step 2")
    # Exercise 2 - Step 2 End


# ---------------------------------------------------------------------------
# Helpers — already implemented, do not modify
# ---------------------------------------------------------------------------

def _chunk(text: str, size: int = 800, overlap: int = 100) -> Iterable[str]:
    """Yield overlapping character-based chunks of `text`.

    800-char windows with 100-char overlap is a practical default for
    Markdown / prose. Switch to `tiktoken`-based chunking if you need
    token-accurate budgets, but character windows are enough for this lab.
    """
    text = text.strip()
    if not text:
        return
    if len(text) <= size:
        yield text
        return
    start = 0
    step = max(1, size - overlap)
    while start < len(text):
        end = min(start + size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            yield chunk
        if end == len(text):
            break
        start += step


def _embed(texts: list[str]) -> list[list[float]]:
    """Embed a batch of strings via the Foundry project's OpenAI client.

    Returns one 1536-dim vector per input string. Uses `DefaultAzureCredential`
    to authenticate against the Foundry project endpoint, so whichever Azure
    identity is logged in must have the `Azure AI User` role on the project
    (the lab's `AzureAIUser` credential already has this).
    """
    if not texts:
        return []
    with AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=CRED) as project:
        with project.get_openai_client() as client:
            resp = client.embeddings.create(
                model=EMBEDDING_DEPLOYMENT,
                input=texts,
            )
    return [item.embedding for item in resp.data]


# ---------------------------------------------------------------------------
# CLI entry point: `python -m app.retrieval <ingest|search> [query]`
# ---------------------------------------------------------------------------

def _main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: python -m app.retrieval <ingest|search> [query]")
        return 1
    cmd = argv[1]
    if cmd == "ingest":
        ingest()
        return 0
    if cmd == "search":
        if len(argv) < 3:
            print("usage: python -m app.retrieval search \"<query>\"")
            return 1
        query = " ".join(argv[2:])
        hits = search(query)
        print(json.dumps(hits, indent=2))
        return 0
    print(f"unknown command: {cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
