"""Exercise 2 (part 1) — build the RAG index over Summitline product docs.

Creates (or replaces) the vector index the Foundry agent will search.
Uses text-embedding-3-large deployed on the same Foundry account.

Index schema:
    id (key)         string
    title            string
    content          string
    contentVector    Collection(Single), dims=3072  (text-embedding-3-large)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from azure.identity import DefaultAzureCredential
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
from openai import AzureOpenAI

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "data" / "product_docs"


def _embed_client() -> AzureOpenAI:
    # The Foundry account exposes Azure OpenAI at
    # <name>.openai.azure.com — same account, different data plane.
    cred = DefaultAzureCredential()

    def _token_provider() -> str:
        return cred.get_token("https://cognitiveservices.azure.com/.default").token

    return AzureOpenAI(
        api_version="2024-10-21",
        azure_endpoint=os.environ["AZURE_SPEECH_ENDPOINT"]
            .replace(".services.ai.azure.com", ".openai.azure.com")
            .replace(".cognitiveservices.azure.com", ".openai.azure.com"),
        azure_ad_token_provider=_token_provider,
    )


def _embed(client: AzureOpenAI, texts: list[str]) -> list[list[float]]:
    resp = client.embeddings.create(
        input=texts, model=os.environ["EMBEDDING_DEPLOYMENT"]
    )
    return [d.embedding for d in resp.data]


def main() -> int:
    endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
    index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
    cred = DefaultAzureCredential()

    idx_client = SearchIndexClient(endpoint=endpoint, credential=cred)

    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="title", type=SearchFieldDataType.String, filterable=True),
        SearchField(
            name="content",
            type=SearchFieldDataType.String,
            searchable=True,
        ),
        SearchField(
            name="contentVector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=3072,
            vector_search_profile_name="hnsw-profile",
        ),
    ]
    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="hnsw-config")],
        profiles=[VectorSearchProfile(name="hnsw-profile", algorithm_configuration_name="hnsw-config")],
    )
    idx_client.create_or_update_index(
        SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
    )
    print(f"Index {index_name} ready.")

    docs, texts = [], []
    for md in sorted(DOCS_DIR.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        title = text.splitlines()[0].lstrip("# ").strip()
        docs.append({"id": md.stem, "title": title, "content": text})
        texts.append(text)
    print(f"Read {len(docs)} product docs.")

    aoai = _embed_client()
    vectors = _embed(aoai, texts)
    for d, v in zip(docs, vectors):
        d["contentVector"] = v

    search = SearchClient(endpoint=endpoint, index_name=index_name, credential=cred)
    result = search.upload_documents(documents=docs)
    ok = sum(1 for r in result if r.succeeded)
    print(f"Uploaded {ok}/{len(docs)} docs to {index_name}.")
    return 0 if ok == len(docs) else 3


if __name__ == "__main__":
    sys.exit(main())
