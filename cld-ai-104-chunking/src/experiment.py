"""Exercise 2 — measure retrieval quality across 5 chunking configurations."""

import json
import math
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chunkers import fixed_size, recursive_split, no_split


DATA = Path(__file__).resolve().parent.parent / "data"
RUNBOOK = (DATA / "runbook.md").read_text(encoding="utf-8")
QUERIES = json.loads((DATA / "queries.json").read_text(encoding="utf-8"))


CONFIGS = [
    {"name": "no-split", "fn": lambda t: no_split(t)},
    {"name": "fixed-200", "fn": lambda t: fixed_size(t, 200)},
    {"name": "fixed-500", "fn": lambda t: fixed_size(t, 500)},
    {"name": "fixed-1000", "fn": lambda t: fixed_size(t, 1000)},
    {"name": "recursive-500-100", "fn": lambda t: recursive_split(t, 500, 100)},
]


# Simple TF-IDF retriever (no embedding dependency).
def _tokenize(s: str) -> list[str]:
    return re.findall(r"\b[a-z0-9]{2,}\b", s.lower())


def _build_index(chunks: list[str]):
    df = Counter()
    tokens = [_tokenize(c) for c in chunks]
    for toks in tokens:
        for t in set(toks):
            df[t] += 1
    n = len(chunks)
    idf = {t: math.log((n + 1) / (df_count + 1)) + 1 for t, df_count in df.items()}
    doc_vecs = []
    for toks in tokens:
        tf = Counter(toks)
        vec = {t: (tf[t] / max(len(toks), 1)) * idf.get(t, 0) for t in tf}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        doc_vecs.append({t: v / norm for t, v in vec.items()})
    return idf, doc_vecs


def _retrieve(query: str, chunks: list[str], idf: dict, doc_vecs: list[dict], k: int = 3):
    toks = _tokenize(query)
    tf = Counter(toks)
    q_vec = {t: (tf[t] / max(len(toks), 1)) * idf.get(t, 0) for t in tf}
    norm = math.sqrt(sum(v * v for v in q_vec.values())) or 1.0
    q_vec = {t: v / norm for t, v in q_vec.items()}
    scored = []
    for i, d_vec in enumerate(doc_vecs):
        sim = sum(q_vec.get(t, 0) * d_vec.get(t, 0) for t in q_vec)
        scored.append((sim, i))
    scored.sort(reverse=True)
    return [chunks[i] for sim, i in scored[:k] if sim > 0]


def main() -> int:
    print(f"experiment: {len(CONFIGS)} chunking configs x {len(QUERIES)} queries\n")

    # TODO: for each config, chunk the runbook, build TF-IDF index, run each query,
    # and check whether the expected_substring appears in the top-k retrieved chunks.
    # Report per-config: chunk count, avg chunk size, precision@1 (top-1 hit), recall@3.
    #
    # HINT:
    #   print(f"{'config':<20} {'chunks':<8} {'avg_len':<9} {'P@1':<6} {'R@3':<6}")
    #   for cfg in CONFIGS:
    #       chunks = cfg["fn"](RUNBOOK)
    #       idf, dv = _build_index(chunks)
    #       hits_at_1 = 0; hits_at_3 = 0
    #       for q in QUERIES:
    #           top3 = _retrieve(q["q"], chunks, idf, dv, k=3)
    #           if top3 and q["expected_substring"] in top3[0]: hits_at_1 += 1
    #           if any(q["expected_substring"] in c for c in top3): hits_at_3 += 1
    #       n = len(QUERIES)
    #       avg_len = sum(len(c) for c in chunks) // max(len(chunks), 1)
    #       print(f"{cfg['name']:<20} {len(chunks):<8} {avg_len:<9} "
    #             f"{hits_at_1}/{n}    {hits_at_3}/{n}")
    #   print("\nInterpretation: recursive-500 usually wins precision without losing recall.")
    raise NotImplementedError("TODO: implement the experiment loop")


if __name__ == "__main__":
    sys.exit(main())
