"""Index, ingest, and retrieve over Azure AI Search.

CLI:
    python -m app.retrieval ingest    # build index + ingest sample_docs/
    python -m app.retrieval search "what is RAG?"
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterable

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
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
INDEX = os.environ["AZURE_SEARCH_INDEX"]
PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
EMBEDDING_DEPLOYMENT = os.environ["EMBEDDING_DEPLOYMENT"]

CRED = DefaultAzureCredential()
HERE = Path(__file__).resolve().parent.parent
SAMPLE_DOCS = HERE / "sample_docs"


def _embed(texts: list[str]) -> list[list[float]]:
    """Embed texts via the Foundry-deployed embedding model."""
    with AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=CRED) as project:
        with project.get_openai_client() as client:
            res = client.embeddings.create(model=EMBEDDING_DEPLOYMENT, input=texts)
            return [d.embedding for d in res.data]


def _chunk(text: str, size: int = 800, overlap: int = 100) -> Iterable[str]:
    i = 0
    while i < len(text):
        yield text[i:i + size]
        i += size - overlap


def create_index() -> None:
    # TODO 1: Build a SearchIndex with fields:
    #         - id (Edm.String, key=True)
    #         - source (Edm.String, filterable=True)
    #         - chunk (Edm.String, searchable=True)
    #         - embedding (Collection(Edm.Single), vector_search_dimensions=1536,
    #           vector_search_profile_name="default")
    # TODO 2: Add VectorSearch with one HnswAlgorithmConfiguration("default-hnsw")
    #         and VectorSearchProfile("default", algorithm_configuration_name="default-hnsw").
    # TODO 3: Add SemanticSearch with one SemanticConfiguration("default") prioritizing
    #         the `chunk` field.
    # TODO 4: Call SearchIndexClient(ENDPOINT, CRED).create_or_update_index(index).
    raise NotImplementedError


def ingest() -> None:
    # TODO 5: For each .md file in SAMPLE_DOCS, chunk it, embed all chunks, and upload
    #         documents [{"id": f"{name}-{i}", "source": name, "chunk": text, "embedding": vec}].
    raise NotImplementedError


def search(query: str, k: int = 5) -> list[dict]:
    # TODO 6: Embed the query (single item). Construct
    #         VectorizedQuery(vector=vec, k_nearest_neighbors=k, fields="embedding").
    # TODO 7: Call SearchClient(ENDPOINT, INDEX, CRED).search(search_text=query,
    #         vector_queries=[vq], select=["id","source","chunk"], top=k,
    #         query_type="semantic", semantic_configuration_name="default").
    # TODO 8: Return [{"id":..., "source":..., "chunk":..., "score": r["@search.score"]}].
    raise NotImplementedError


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "ingest"
    if cmd == "ingest":
        create_index()
        ingest()
        print("ingested.")
    elif cmd == "search":
        for hit in search(sys.argv[2]):
            print(hit["score"], hit["source"], "→", hit["chunk"][:120])
    else:
        raise SystemExit(f"unknown cmd: {cmd}")
