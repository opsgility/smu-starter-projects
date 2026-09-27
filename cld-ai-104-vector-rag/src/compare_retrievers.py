"""Exercise 3 — compare TF-IDF vs vector retrieval on 8 synonym-heavy queries."""

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vector_index import retrieve as vec_retrieve, CHUNKS
from embedder import is_real_embedder


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\b[a-z0-9]{2,}\b", text.lower())


def _build_tfidf():
    df = Counter()
    doc_tokens = []
    for c in CHUNKS:
        toks = _tokenize(c["text"])
        doc_tokens.append(toks)
        for t in set(toks):
            df[t] += 1
    n = len(CHUNKS)
    idf = {t: math.log((n + 1) / (df_count + 1)) + 1 for t, df_count in df.items()}
    doc_vecs = []
    for toks in doc_tokens:
        tf = Counter(toks)
        vec = {t: (tf[t] / max(len(toks), 1)) * idf.get(t, 0) for t in tf}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        doc_vecs.append({t: v / norm for t, v in vec.items()})
    return idf, doc_vecs


_IDF, _DOC_VECS = _build_tfidf()


def tfidf_retrieve(query: str, k: int = 5):
    toks = _tokenize(query)
    tf = Counter(toks)
    q_vec = {t: (tf[t] / max(len(toks), 1)) * _IDF.get(t, 0) for t in tf}
    norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0
    q_vec = {t: v / norm for t, v in q_vec.items()}
    scored = []
    for i, d_vec in enumerate(_DOC_VECS):
        sim = sum(q_vec.get(t, 0) * d_vec.get(t, 0) for t in q_vec)
        scored.append((sim, i))
    scored.sort(reverse=True)
    return [{"score": s, **CHUNKS[i]} for s, i in scored[:k] if s > 0]


# Synonym-heavy queries — the query words don't overlap with the doc words.
QUERIES = [
    {"q": "money back", "expected": "refund-1"},
    {"q": "credit for outage", "expected": "refund-2"},
    {"q": "how urgent must major incidents get fixed", "expected": "sla-1"},
    {"q": "data residency for European clients", "expected": "compliance-1"},
    {"q": "how do I authenticate my API requests", "expected": "api-3"},
    {"q": "audit report request", "expected": "compliance-2"},
    {"q": "keeping analytics data long term", "expected": "compliance-3"},
    {"q": "API endpoint for customer lookup", "expected": "api-2"},
]


def main() -> int:
    print(f"embedder: {'SentenceTransformers (real)' if is_real_embedder() else 'stub (hash-based)'}\n")
    print(f"{'query':<40} {'tfidf top-1':<14} {'vec top-1':<14}  hits_tfidf hits_vec")
    print("-" * 92)
    tfidf_hits = 0
    vec_hits = 0
    for q in QUERIES:
        try:
            t = tfidf_retrieve(q["q"], k=5)
            v = vec_retrieve(q["q"], k=5)
        except NotImplementedError as e:
            print(f"  vector TODO: {e}"); return 1
        t_top = (t[0]["id"] if t else "-")
        v_top = (v[0]["id"] if v else "-")
        t_hit = q["expected"] in [r["id"] for r in t[:5]]
        v_hit = q["expected"] in [r["id"] for r in v[:5]]
        if t_hit: tfidf_hits += 1
        if v_hit: vec_hits += 1
        print(f"{q['q'][:38]:<40} {t_top:<14} {v_top:<14}  {'✓' if t_hit else '✗'}          {'✓' if v_hit else '✗'}")
    n = len(QUERIES)
    print(f"\nSummary: tfidf recall={tfidf_hits}/{n} ({100*tfidf_hits/n:.0f}%)  vec recall={vec_hits}/{n} ({100*vec_hits/n:.0f}%)")
    print("Expected pattern (real embedder): vec beats tfidf by 20-40 points on synonym queries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
