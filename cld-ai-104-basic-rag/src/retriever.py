"""COMPLETE: TF-IDF retriever (stdlib only, no external embedding dep)."""

import json
import math
import re
from collections import Counter
from pathlib import Path

CHUNKS = json.loads((Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json").read_text(encoding="utf-8"))


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\b[a-z0-9]{2,}\b", text.lower())


def _build_index(chunks):
    df = Counter()
    doc_tokens = []
    for c in chunks:
        toks = _tokenize(c["text"])
        doc_tokens.append(toks)
        for t in set(toks):
            df[t] += 1
    n = len(chunks)
    idf = {t: math.log((n + 1) / (df_count + 1)) + 1 for t, df_count in df.items()}
    doc_vectors = []
    for toks in doc_tokens:
        tf = Counter(toks)
        vec = {t: (tf[t] / max(len(toks), 1)) * idf.get(t, 0) for t in tf}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        doc_vectors.append({t: v / norm for t, v in vec.items()})
    return idf, doc_vectors


_IDF, _DOC_VECS = _build_index(CHUNKS)


def _query_vector(query: str):
    toks = _tokenize(query)
    tf = Counter(toks)
    vec = {t: (tf[t] / max(len(toks), 1)) * _IDF.get(t, 0) for t in tf}
    norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
    return {t: v / norm for t, v in vec.items()}


def retrieve(query: str, k: int = 5) -> list[dict]:
    """Return top-k chunks with cosine similarity scores."""
    q_vec = _query_vector(query)
    scores = []
    for i, d_vec in enumerate(_DOC_VECS):
        # Cosine similarity
        s = sum(q_vec.get(t, 0) * d_vec.get(t, 0) for t in q_vec)
        scores.append((s, i))
    scores.sort(reverse=True)
    return [{"score": round(s, 4), **CHUNKS[i]} for s, i in scores[:k] if s > 0]
