"""Exercise 2 — build a vector index + top-k semantic search.

Fill in the TODO to build the index at import time and implement
retrieve() using cosine similarity.

Run standalone: `python src/vector_index.py "money back"`
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from embedder import embed, embed_one, is_real_embedder


CHUNKS = json.loads((Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json").read_text(encoding="utf-8"))

# TODO 1: at import time, build INDEX by calling embed() on each chunk's text.
# Store as list of vectors aligned with CHUNKS.
#
# HINT:
#   INDEX = embed([c["text"] for c in CHUNKS])
INDEX: list[list[float]] = []


def retrieve(query: str, k: int = 5) -> list[dict]:
    """Return top-k chunks by cosine similarity to query."""
    if not INDEX:
        raise RuntimeError("INDEX not built — fill in TODO 1 in vector_index.py")

    q_vec = embed_one(query)

    # TODO 2: compute cosine similarity between q_vec and every vector in INDEX,
    # sort descending, return top k CHUNKS with their scores.
    # Both q_vec and INDEX vectors are already normalized to unit length,
    # so cosine similarity = dot product.
    #
    # HINT:
    #   scored = []
    #   for i, d_vec in enumerate(INDEX):
    #       sim = sum(a * b for a, b in zip(q_vec, d_vec))
    #       scored.append((sim, i))
    #   scored.sort(reverse=True)
    #   return [{"score": round(sim, 4), **CHUNKS[i]} for sim, i in scored[:k]]
    raise NotImplementedError("TODO 2: implement retrieve")


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: vector_index.py \"<query>\""); return 2
    print(f"embedder: {'SentenceTransformers (real)' if is_real_embedder() else 'stub (hash-based, recall will be low)'}")
    hits = retrieve(sys.argv[1], k=5)
    for h in hits:
        print(f"  score={h['score']}  id={h['id']}  text={h['text'][:80]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
