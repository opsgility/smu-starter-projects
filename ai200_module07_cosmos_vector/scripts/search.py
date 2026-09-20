"""Query the vector store with a free-text question."""
from __future__ import annotations

import argparse
import json
import sys

from lib.embeddings import embed
from lib.vector_store import search_similar


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("query", type=str)
    ap.add_argument("--tenant", default=None)
    ap.add_argument("--top-k", type=int, default=5)
    args = ap.parse_args()

    qvec = embed(args.query)
    hits = search_similar(qvec, top_k=args.top_k, tenant=args.tenant)
    print(json.dumps(hits, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
