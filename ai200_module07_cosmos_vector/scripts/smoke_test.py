"""Verify the embeddings + vector_store wiring works end-to-end."""
from __future__ import annotations

import sys

from lib.embeddings import embed
from lib.vector_store import upsert_vector, search_similar


def main() -> int:
    vec = embed("smoke test — package soaked")
    print(f"[ok] embedding dim={len(vec)}")
    upsert_vector(
        item_id="smoke-1",
        tenant="acme",
        text="smoke test — package soaked",
        embedding=vec,
        metadata={"source": "smoke"},
    )
    print("[ok] upsert_vector wrote smoke-1")
    hits = search_similar(vec, top_k=1, tenant="acme")
    print(f"[ok] search_similar returned {len(hits)} hit(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
