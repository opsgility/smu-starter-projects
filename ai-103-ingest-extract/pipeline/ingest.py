"""Ingest pipeline for the Summitline Outfitters knowledge base.

Exercise 2 (Lab 2273 / 3407) asks you to implement `main()`. The helpers
`_chunk` and `_embed` are provided so you can focus on wiring the five
pipeline stages together:

    list blobs -> download -> CU extract -> chunk + embed -> upload

Run with:
    python -m pipeline.ingest
"""
from __future__ import annotations

import json
import os
import re
from typing import Iterable

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchIndexingBufferedSender
from azure.storage.blob import ContainerClient
from dotenv import load_dotenv

from pipeline import cu_extract, index

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
EMBED_DEPLOYMENT = os.environ["EMBEDDING_DEPLOYMENT"]
SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
INDEX = os.environ["AZURE_SEARCH_INDEX"]
ACCOUNT = os.environ["AZURE_STORAGE_ACCOUNT"]
CONTAINER = os.environ["AZURE_STORAGE_CONTAINER"]

# Tuning constants for markdown chunking. ~1,500 chars keeps each chunk well
# under a single embedding request's token budget while preserving enough
# context for the reranker.
_CHUNK_TARGET = 1500
_CHUNK_OVERLAP = 150


# ---------------------------------------------------------------------------
# Helpers (provided)
# ---------------------------------------------------------------------------

def _chunk(markdown: str) -> Iterable[str]:
    """Split markdown into overlapping ~1,500 char chunks along paragraph
    boundaries.

    This helper is provided. Exercise 2 only asks you to wire `main()`; you
    do not need to change the chunking logic.
    """
    if not markdown:
        return

    # Normalize line endings so paragraph splitting is deterministic.
    text = re.sub(r"\r\n?", "\n", markdown).strip()
    if not text:
        return

    paragraphs = [p.strip() for p in re.split(r"\n{2,}", text) if p.strip()]

    buf: list[str] = []
    size = 0
    for para in paragraphs:
        if size + len(para) + 2 > _CHUNK_TARGET and buf:
            chunk = "\n\n".join(buf)
            yield chunk
            # Start next buffer with a small tail overlap for context continuity.
            tail = chunk[-_CHUNK_OVERLAP:] if len(chunk) > _CHUNK_OVERLAP else chunk
            buf = [tail, para]
            size = len(tail) + len(para) + 2
        else:
            buf.append(para)
            size += len(para) + 2

    if buf:
        yield "\n\n".join(buf)


def _embed(chunks: list[str]) -> list[list[float]]:
    """Batch-embed a list of chunks in a single request.

    `text-embedding-3-large` emits 3072-dim vectors. Do NOT pass a
    `dimensions` override - the index field is sized to 3072.
    """
    client = AIProjectClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(),
    ).get_openai_client()
    resp = client.embeddings.create(model=EMBED_DEPLOYMENT, input=chunks)
    return [d.embedding for d in resp.data]


# ---------------------------------------------------------------------------
# Pipeline entry-point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the Summitline ingest pipeline end-to-end.

    Stages:
      1. Ensure the CU analyzer and the Search index exist.
      2. List blobs in AZURE_STORAGE_CONTAINER with DefaultAzureCredential.
      3. For each blob:
           - download bytes
           - call cu_extract.extract() -> {"markdown", "fields"}
           - flatten CU envelopes (valueString / valueNumber / valueBoolean)
           - _chunk() the markdown
           - _embed() the chunks in one batch
           - build a document per chunk with the shape expected by the index
           - sender.upload_documents(documents)
      4. Explicitly sender.flush() before leaving the `with` block and
         report sender.failed_count.
    """
    # TODO (Exercise 2 Step 4): Implement the pipeline body as described in
    # the docstring above. Use `SearchIndexingBufferedSender` as the uploader
    # and remember the explicit `.flush()` call before the context exits.
    raise NotImplementedError("Implement main() in Exercise 2 Step 4.")


if __name__ == "__main__":
    main()
