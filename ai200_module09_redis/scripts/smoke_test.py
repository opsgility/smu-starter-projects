"""Confirm Redis, cache, and vector index are wired correctly."""
from __future__ import annotations

import sys

from lib.cache import cached_call
from lib.embeddings import embed
from lib.redis_client import get_redis
from lib.vector_index import create_index, knn_search, upsert_doc


def main() -> int:
    r = get_redis()
    assert r.ping() is True
    print("[ok] redis PING")

    # Cache
    text, hit = cached_call("hello world", lambda p: f"echo: {p}", ttl_seconds=30)
    assert text.startswith("echo:")
    print(f"[ok] cache miss returned text=({text}) hit={hit}")
    text, hit = cached_call("hello world", lambda p: f"echo: {p}", ttl_seconds=30)
    assert hit is True
    print(f"[ok] cache hit returned text=({text}) hit={hit}")

    # Vector
    create_index()
    v = embed("smoke test — package soaked")
    upsert_doc("smoke-1", "acme", "sop", "smoke test — package soaked", v)
    hits = knn_search(v, top_k=1, tenant="acme")
    assert hits
    print(f"[ok] knn_search returned {hits[0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
