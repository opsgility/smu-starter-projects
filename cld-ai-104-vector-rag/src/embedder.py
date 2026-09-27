"""Embedder wrapper — uses SentenceTransformers if available, else deterministic stub.

The stub is NOT a real embedder — it's a hash-based bag-of-features vector.
Recall on synonym queries will be low with the stub. Install
sentence-transformers for realistic results:
    pip install sentence-transformers
"""

import hashlib
import math

_USE_ST = False
_ST_MODEL = None

try:
    from sentence_transformers import SentenceTransformer
    _ST_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    _USE_ST = True
except Exception:
    pass


def is_real_embedder() -> bool:
    return _USE_ST


def _stub_embed(text: str, dim: int = 384) -> list[float]:
    """Deterministic bag-of-hashed-token-features embedder."""
    tokens = text.lower().split()
    vec = [0.0] * dim
    for tok in tokens:
        h = int(hashlib.sha256(tok.encode()).hexdigest(), 16)
        vec[h % dim] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def embed(texts: list[str]) -> list[list[float]]:
    if _USE_ST:
        return _ST_MODEL.encode(texts, normalize_embeddings=True).tolist()
    return [_stub_embed(t) for t in texts]


def embed_one(text: str) -> list[float]:
    return embed([text])[0]
