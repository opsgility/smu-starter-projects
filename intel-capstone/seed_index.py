"""Seed the ``sib-osint-kb`` Azure AI Search index with sample SIB docs.

Run once after Exercise 1 Step 5 has created the index schema:

    python seed_index.py

Reads every ``.md`` file under ``sample_docs/``, generates a
``text-embedding-3-large`` embedding (3072-dim) for each, and uploads a
document with the fields ``id``, ``source``, ``markdown``, ``embedding``.

Note on the two-client split: embeddings go directly to the Azure OpenAI
(account-scoped) endpoint via the ``AzureOpenAI`` client because the
Foundry project endpoint does not currently route embeddings requests
(it only routes chat/responses/agents). See MS Learn:
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

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from openai import AzureOpenAI

AOAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
EMBEDDING = os.environ.get("EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
SEARCH_ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT")
INDEX = os.environ.get("AZURE_SEARCH_INDEX", "sib-osint-kb")

SAMPLE_DIR = Path(__file__).parent / "sample_docs"


def _slug_id(source: str) -> str:
    """Stable, URL-safe doc id derived from the file name."""
    return hashlib.sha1(source.encode("utf-8")).hexdigest()[:16]


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
