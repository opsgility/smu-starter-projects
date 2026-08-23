"""Index Ridgevault research docs into Azure AI Search.

Reads every markdown file under `data/research/`, chunks it into ~800-token
sections with a small overlap, embeds each chunk with the Foundry-hosted
embedding model, and uploads the {id, title, chunk, vector} documents into the
Azure AI Search index named by SEARCH_INDEX_NAME.

Exercise 4 — implement the create-index-if-missing + upload loop per the
docstring contract. All infrastructure (Foundry, Search service, Storage
account + container) is provisioned by the lab's ARM template.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path
from typing import Iterable, List

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    VectorSearch,
    VectorSearchProfile,
)
from dotenv import load_dotenv


DATA_ROOT = Path(__file__).resolve().parent.parent.parent / "data" / "research"
CHUNK_TOKENS = 800
CHUNK_OVERLAP = 80


def _chunk(text: str, size: int, overlap: int) -> List[str]:
    """Naive whitespace-aware chunker sized in ~words (not tokens) as a stand-in.

    Exercise 4 does not require you to change this — the chunker is a starter
    convenience. Real Ridgevault production uses a token-aware splitter.
    """
    words = text.split()
    if not words:
        return []
    chunks: List[str] = []
    step = max(1, size - overlap)
    for i in range(0, len(words), step):
        chunks.append(" ".join(words[i : i + size]))
        if i + size >= len(words):
            break
    return chunks


def iter_docs() -> Iterable[tuple[str, str]]:
    """Yield (doc_id, markdown_text) for every seed doc under data/research/."""
    for path in sorted(DATA_ROOT.glob("*.md")):
        yield path.stem, path.read_text(encoding="utf-8")


def ensure_index(index_client: SearchIndexClient, index_name: str) -> None:
    """Create the index if it doesn't exist. Idempotent."""
    try:
        index_client.get_index(index_name)
        return
    except Exception:
        pass

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="title", type=SearchFieldDataType.String, filterable=True),
        SearchField(name="chunk", type=SearchFieldDataType.String, searchable=True),
        SearchField(
            name="vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="ridgevault-hnsw",
        ),
    ]
    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="ridgevault-hnsw-algo")],
        profiles=[
            VectorSearchProfile(
                name="ridgevault-hnsw",
                algorithm_configuration_name="ridgevault-hnsw-algo",
            )
        ],
    )
    index_client.create_index(
        SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
    )


def main() -> int:
    load_dotenv()
    endpoint = os.environ["SEARCH_ENDPOINT"]
    index_name = os.environ["SEARCH_INDEX_NAME"]

    credential = DefaultAzureCredential()
    index_client = SearchIndexClient(endpoint=endpoint, credential=credential)
    ensure_index(index_client, index_name)

    search_client = SearchClient(
        endpoint=endpoint, index_name=index_name, credential=credential
    )

    # TODO (Exercise 4): For every (doc_id, text) from iter_docs():
    #   1. Chunk via _chunk(text, CHUNK_TOKENS, CHUNK_OVERLAP).
    #   2. Embed each chunk against the Foundry embedding endpoint using the same
    #      bearer-token pattern as verify_env.py (base_url = FOUNDRY_PROJECT_ENDPOINT + /openai/v1).
    #   3. Assemble documents of shape:
    #        {"id": f"{doc_id}-{i}", "title": doc_id, "chunk": text, "vector": embedding}
    #   4. Upload in batches of 100 via search_client.upload_documents(batch).
    # Wire below.

    docs = list(iter_docs())
    if not docs:
        print(f"ERROR: no seed docs under {DATA_ROOT}", file=sys.stderr)
        return 1

    print(f"Found {len(docs)} seed docs. Implement the upload loop per Exercise 4.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
