"""Create a vector-search AI Search index and upload one document per CU segment.

Implemented across Exercise 5 TODOs 1-4.

Index schema (Summitline video-segments):

    id                (String, key)                = "<video>_<start_ms>"
    video_id          (String, filterable)
    start_ms          (Int64,  filterable, sortable)
    end_ms            (Int64)
    scene_summary     (String, searchable)
    products          (Collection<String>, filterable)
    presenter_quality (String, filterable)
    embedding         (Collection<Single>, vector, 3072 dims, hnsw)

We embed `scene_summary` with `text-embedding-3-large` (default 3072 dims) and
run vector queries against `embedding`.

Run with:
    python src/index_segments.py
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
from typing import Any, Dict, Iterable, List

from dotenv import load_dotenv

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
from openai import AzureOpenAI


load_dotenv()

SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
INDEX_NAME = os.environ["AZURE_SEARCH_INDEX_NAME"]
EMBEDDING_DEPLOYMENT = os.environ["EMBEDDING_DEPLOYMENT"]
VECTOR_DIMS = 3072  # text-embedding-3-large default
RESULTS_DIR = pathlib.Path(__file__).parent.parent / "data"


def build_index_client() -> SearchIndexClient:
    """AAD-authenticated management client for the AI Search service."""
    return SearchIndexClient(endpoint=SEARCH_ENDPOINT, credential=DefaultAzureCredential())


def build_search_client() -> SearchClient:
    """AAD-authenticated document-plane client scoped to INDEX_NAME."""
    return SearchClient(endpoint=SEARCH_ENDPOINT, index_name=INDEX_NAME,
                        credential=DefaultAzureCredential())


def build_openai_client() -> AzureOpenAI:
    """Keyless Azure OpenAI client rooted at the Foundry account (not the project)."""
    project = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    base = project.split("/api/projects/")[0]
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )
    return AzureOpenAI(api_version="2024-10-21", azure_endpoint=base,
                       azure_ad_token_provider=token_provider)


def create_index(client: SearchIndexClient) -> None:
    """Create the vector index if it does not already exist."""
    # Exercise 5 - TODO 1
    raise NotImplementedError(
        "Exercise 5 TODO 1: build a SearchIndex named INDEX_NAME with the fields listed "
        "in the module docstring, wire VectorSearch(algorithms=[HnswAlgorithmConfiguration(...)], "
        "profiles=[VectorSearchProfile(...)]), then client.create_or_update_index(index)."
    )


def embed(client: AzureOpenAI, text: str) -> List[float]:
    """Embed one string with the deployment named in EMBEDDING_DEPLOYMENT."""
    # Exercise 5 - TODO 2
    raise NotImplementedError(
        "Exercise 5 TODO 2: call client.embeddings.create(model=EMBEDDING_DEPLOYMENT, input=text) "
        "and return response.data[0].embedding."
    )


def _iter_segments(analyzer_result: Dict[str, Any], video_id: str) -> Iterable[Dict[str, Any]]:
    """Flatten the CU analyzer response into one doc per segment.

    CU pro-mode responses put each segment under `result.contents[i]` with
    `startTimeMs`, `endTimeMs`, and a `fields` dict keyed by the field names
    declared in `analyzer_schema.json`.
    """
    for i, seg in enumerate(analyzer_result.get("result", {}).get("contents", [])):
        fields = seg.get("fields", {}) or {}

        def _val(name: str, default: Any = None) -> Any:
            f = fields.get(name)
            if not f:
                return default
            return f.get("valueString") or f.get("valueNumber") or f.get("valueArray") or default

        start_ms = int(seg.get("startTimeMs") or 0)
        end_ms = int(seg.get("endTimeMs") or 0)
        products_raw = _val("products_demonstrated", []) or []
        products = [
            p.get("valueString", p) if isinstance(p, dict) else str(p)
            for p in products_raw
        ]
        yield {
            "id": f"{video_id}_{start_ms:09d}_{i:03d}",
            "video_id": video_id,
            "start_ms": start_ms,
            "end_ms": end_ms,
            "scene_summary": _val("scene_summary", "") or "",
            "products": products,
            "presenter_quality": _val("presenter_quality", "unknown") or "unknown",
        }


def build_docs(analyzer_files: List[pathlib.Path], openai_client: AzureOpenAI) -> List[Dict[str, Any]]:
    """Read every analyzer result JSON and produce ready-to-upload search docs."""
    # Exercise 5 - TODO 3
    raise NotImplementedError(
        "Exercise 5 TODO 3: for each analyzer_files entry, json.load it, derive video_id from "
        "the filename (analyzer_result_<video_id>.json), iterate _iter_segments(), embed the "
        "scene_summary via embed(openai_client, doc['scene_summary']), attach doc['embedding'], "
        "and return the flat list."
    )


def upload_docs(client: SearchClient, docs: List[Dict[str, Any]]) -> None:
    """Batch-upload the segment documents to the index."""
    # Exercise 5 - TODO 4
    raise NotImplementedError(
        "Exercise 5 TODO 4: client.upload_documents(documents=docs) and print how many succeeded "
        "(count results where r.succeeded is True)."
    )


def main() -> None:
    if not RESULTS_DIR.exists() or not list(RESULTS_DIR.glob("analyzer_result_*.json")):
        print("[error] No analyzer_result_*.json files found in data/. "
              "Run src/invoke_analyzer.py first (Exercise 4).", file=sys.stderr)
        sys.exit(3)

    create_index(build_index_client())
    openai_client = build_openai_client()

    files = sorted(RESULTS_DIR.glob("analyzer_result_*.json"))
    docs = build_docs(files, openai_client)
    print(f"[built]    {len(docs)} segment document(s) from {len(files)} video(s)")

    upload_docs(build_search_client(), docs)


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as exc:
        print(f"\n[TODO]     {exc}", file=sys.stderr)
        sys.exit(2)
