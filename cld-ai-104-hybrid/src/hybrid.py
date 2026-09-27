"""Exercise 2 — build hybrid retriever with RRF + stub reranker."""

import hashlib
import json
import math
import sys
from pathlib import Path


CHUNKS = json.loads((Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json").read_text(encoding="utf-8"))


# --- BM25 (using rank_bm25 if available, else stub) ---
try:
    from rank_bm25 import BM25Okapi
    _tokenized = [c["text"].lower().split() for c in CHUNKS]
    _bm25 = BM25Okapi(_tokenized)
except Exception:
    _bm25 = None


def bm25_ranking(query: str) -> list[int]:
    """Return chunk indices ordered best-first by BM25."""
    if _bm25 is None:
        # Fallback: keyword-overlap count
        q_toks = set(query.lower().split())
        scores = [(sum(1 for t in c["text"].lower().split() if t in q_toks), i) for i, c in enumerate(CHUNKS)]
        scores.sort(reverse=True)
        return [i for _, i in scores]
    scores = _bm25.get_scores(query.lower().split())
    return sorted(range(len(CHUNKS)), key=lambda i: -scores[i])


# --- Vector (SentenceTransformers if available, else hash stub) ---
try:
    from sentence_transformers import SentenceTransformer
    _st = SentenceTransformer("all-MiniLM-L6-v2")
    _vec_index = _st.encode([c["text"] for c in CHUNKS], normalize_embeddings=True).tolist()
    _st_ok = True
except Exception:
    _st_ok = False
    _vec_index = None


def _hash_embed(text: str, dim: int = 384) -> list[float]:
    vec = [0.0] * dim
    for tok in text.lower().split():
        h = int(hashlib.sha256(tok.encode()).hexdigest(), 16)
        vec[h % dim] += 1.0
    n = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / n for v in vec]


def vector_ranking(query: str) -> list[int]:
    if _st_ok:
        q = _st.encode([query], normalize_embeddings=True).tolist()[0]
        sims = [sum(a * b for a, b in zip(q, v)) for v in _vec_index]
    else:
        q = _hash_embed(query)
        vecs = [_hash_embed(c["text"]) for c in CHUNKS]
        sims = [sum(a * b for a, b in zip(q, v)) for v in vecs]
    return sorted(range(len(CHUNKS)), key=lambda i: -sims[i])


# --- RRF ---
def rrf_ranking(query: str, k_const: int = 60) -> list[int]:
    """TODO: implement Reciprocal Rank Fusion combining bm25 and vector."""
    # HINT:
    #   b = bm25_ranking(query)
    #   v = vector_ranking(query)
    #   rrf = {i: 0.0 for i in range(len(CHUNKS))}
    #   for rank_i, i in enumerate(b): rrf[i] += 1 / (k_const + rank_i)
    #   for rank_i, i in enumerate(v): rrf[i] += 1 / (k_const + rank_i)
    #   return sorted(rrf.keys(), key=lambda i: -rrf[i])
    raise NotImplementedError("TODO: implement RRF")


# --- Stub reranker (semantic-similarity based) ---
def rerank(query: str, candidate_ids: list[int], top_k: int = 5) -> list[int]:
    """Stub cross-encoder: re-scores candidates by simple query-chunk word overlap.
    Real production: use Voyage rerank-2 or Cohere Rerank cross-encoder.
    """
    q_toks = set(query.lower().split())
    scored = []
    for i in candidate_ids:
        c_toks = set(CHUNKS[i]["text"].lower().split())
        overlap = len(q_toks & c_toks) / max(len(q_toks), 1)
        # Also boost if any query term appears verbatim (exact-term wins)
        exact_bonus = sum(1 for t in q_toks if t in CHUNKS[i]["text"].lower()) * 0.1
        scored.append((overlap + exact_bonus, i))
    scored.sort(reverse=True)
    return [i for _, i in scored[:top_k]]


def hybrid_with_rerank(query: str, k: int = 5, wide: int = 10) -> list[int]:
    """Retrieve top-wide via RRF, then rerank down to top-k."""
    wide_candidates = rrf_ranking(query)[:wide]
    return rerank(query, wide_candidates, top_k=k)
