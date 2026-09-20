"""Create (if missing) and seed the ``sib-osint-kb`` Azure AI Search index.

Run once after ``.env`` is filled in:

    python seed_index.py

The script is idempotent: it creates the index schema on first run and
re-uploads documents on subsequent runs (Search treats uploads as upserts
keyed on ``id``).

Index schema:
  - id        (String, key)
  - source    (String, filterable + sortable)
  - markdown  (String, searchable — full document text used for BM25)
  - embedding (Collection[Single], 3072-dim vector, searchable)
  - VectorSearch: HNSW algorithm + profile named ``default``
  - SemanticSearch: configuration named ``default``, content field ``markdown``

For each ``.md`` file under ``sample_docs/`` the script generates a
``text-embedding-3-large`` embedding and uploads a document with the fields
above.

Two-client split: embeddings go directly to the Azure OpenAI (account-scoped)
endpoint via the ``AzureOpenAI`` client because the Foundry project endpoint
does not currently route embeddings requests (it only routes
chat/responses/agents). See MS Learn:
https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/embeddings
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from azure.core.credentials import TokenCredential
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
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
from openai import AzureOpenAI

AOAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
EMBEDDING = os.environ.get("EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
SEARCH_ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT")
INDEX = os.environ.get("AZURE_SEARCH_INDEX", "sib-osint-kb")
EMBED_DIMENSIONS = 3072

SAMPLE_DIR = Path(__file__).parent / "sample_docs"


def _slug_id(source: str) -> str:
    """Stable, URL-safe doc id derived from the file name."""
    return hashlib.sha1(source.encode("utf-8")).hexdigest()[:16]


def _ensure_index(cred: TokenCredential) -> None:
    """Create the ``sib-osint-kb`` index if it doesn't already exist.

    Idempotent: uses ``create_or_update_index`` under the hood so a re-run
    with an unchanged schema is a no-op.
    """
    client = SearchIndexClient(endpoint=SEARCH_ENDPOINT, credential=cred)
    try:
        client.get_index(INDEX)
        print(f"Index '{INDEX}' already exists — reusing it.")
        return
    except ResourceNotFoundError:
        pass  # fall through to create

    fields = [
        SearchField(name="id", type=SearchFieldDataType.String, key=True),
        SearchField(
            name="source",
            type=SearchFieldDataType.String,
            filterable=True,
            sortable=True,
        ),
        SearchField(name="markdown", type=SearchFieldDataType.String, searchable=True),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=EMBED_DIMENSIONS,
            vector_search_profile_name="default",
        ),
    ]
    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="hnsw")],
        profiles=[
            VectorSearchProfile(name="default", algorithm_configuration_name="hnsw")
        ],
    )
    semantic = SemanticSearch(
        configurations=[
            SemanticConfiguration(
                name="default",
                prioritized_fields=SemanticPrioritizedFields(
                    content_fields=[SemanticField(field_name="markdown")],
                ),
            )
        ]
    )
    index = SearchIndex(
        name=INDEX,
        fields=fields,
        vector_search=vector_search,
        semantic_search=semantic,
    )
    client.create_or_update_index(index)
    print(f"Created index '{INDEX}'.")


def main() -> int:
    if not AOAI_ENDPOINT or not SEARCH_ENDPOINT:
        print(
            "error: AZURE_OPENAI_ENDPOINT and AZURE_SEARCH_ENDPOINT must be set. "
            "Did you run Exercise 1 Step 3?",
            file=sys.stderr,
        )
        return 2

    if not SAMPLE_DIR.exists():
        print(f"error: sample_docs/ not found at {SAMPLE_DIR}", file=sys.stderr)
        return 2

    cred = DefaultAzureCredential()

    _ensure_index(cred)

    token_provider = get_bearer_token_provider(
        cred, "https://cognitiveservices.azure.com/.default"
    )
    aoai = AzureOpenAI(
        azure_endpoint=AOAI_ENDPOINT,
        api_version="2024-10-21",
        azure_ad_token_provider=token_provider,
    )

    docs: list[dict] = []
    for md_path in sorted(SAMPLE_DIR.glob("*.md")):
        text = md_path.read_text(encoding="utf-8")
        emb = aoai.embeddings.create(model=EMBEDDING, input=[text]).data[0].embedding
        assert len(emb) == 3072, f"Expected 3072-dim embedding, got {len(emb)}"
        docs.append(
            {
                "id": _slug_id(md_path.name),
                "source": md_path.name,
                "markdown": text,
                "embedding": emb,
            }
        )

    search = SearchClient(endpoint=SEARCH_ENDPOINT, index_name=INDEX, credential=cred)
    result = search.upload_documents(documents=docs)
    succeeded = sum(1 for r in result if r.succeeded)
    print(f"Uploaded {succeeded} documents to {INDEX}")

    failures = [r for r in result if not r.succeeded]
    if failures:
        for r in failures:
            print(f"  FAILED id={r.key} status={r.status_code} error={r.error_message}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
