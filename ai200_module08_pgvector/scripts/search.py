"""CLI for the RAG retrieval step."""
from __future__ import annotations

import argparse
import json
import sys

from lib.embeddings import embed
from lib.rag import search_with_filter


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--tenant", required=True)
    ap.add_argument("--category", default=None)
    ap.add_argument("--top-k", type=int, default=5)
    args = ap.parse_args()
    qv = embed(args.query)
    hits = search_with_filter(qv, tenant=args.tenant, category=args.category, top_k=args.top_k)
    for h in hits:
        h["distance"] = float(h.get("distance", 0))
    print(json.dumps(hits, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
