"""Confirm pg.get_conn(), rag.upsert_doc, rag.search_with_filter all work."""
from __future__ import annotations

import sys

from lib.embeddings import embed
from lib.pg import get_conn
from lib.rag import search_with_filter, upsert_doc


def main() -> int:
    # 1. Connection
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT 1;")
        assert cur.fetchone()[0] == 1
    print("[ok] pg.get_conn returns a working connection")

    # 2. Upsert a single test row
    vec = embed("smoke test — package soaked from rain")
    upsert_doc(
        doc_id="smoke-1",
        tenant="acme",
        text="smoke test — package soaked from rain",
        embedding=vec,
        metadata={"category": "smoke"},
    )
    print("[ok] upsert_doc wrote smoke-1")

    # 3. Search
    hits = search_with_filter(vec, tenant="acme", category="smoke", top_k=1)
    assert hits and hits[0]["id"] == "smoke-1"
    print(f"[ok] search_with_filter returned smoke-1, distance={hits[0]['distance']:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
