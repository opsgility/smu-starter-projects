"""COMPLETE: chunker + BM25 retriever + cited Claude generation."""

import hashlib
import json
import math
import os
import re
import sys
from collections import Counter
from pathlib import Path

import anthropic


DATA = Path(__file__).resolve().parent.parent / "data"
CORPUS = (DATA / "corpus.md").read_text(encoding="utf-8")


def recursive_split(text: str, max_chars: int = 400) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    paras = text.split("\n\n")
    chunks, cur = [], ""
    for p in paras:
        candidate = f"{cur}\n\n{p}" if cur else p
        if len(candidate) <= max_chars:
            cur = candidate
        else:
            if cur:
                chunks.append(cur)
            cur = p
    if cur:
        chunks.append(cur)
    return chunks


CHUNKS = [{"id": f"chunk-{i}", "text": t} for i, t in enumerate(recursive_split(CORPUS))]


# BM25-lite (rank_bm25-free) — TF-IDF cosine
def _tokenize(s: str) -> list[str]:
    return re.findall(r"\b[a-z0-9]{2,}\b", s.lower())


def _build_index(chunks):
    df = Counter()
    docs = [_tokenize(c["text"]) for c in chunks]
    for toks in docs:
        for t in set(toks):
            df[t] += 1
    n = len(chunks)
    idf = {t: math.log((n + 1) / (v + 1)) + 1 for t, v in df.items()}
    vecs = []
    for toks in docs:
        tf = Counter(toks)
        v = {t: (tf[t] / max(len(toks), 1)) * idf.get(t, 0) for t in tf}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs.append({t: x / norm for t, x in v.items()})
    return idf, vecs


_IDF, _DOC_VECS = _build_index(CHUNKS)


def retrieve(query: str, k: int = 4) -> list[dict]:
    toks = _tokenize(query)
    tf = Counter(toks)
    q = {t: (tf[t] / max(len(toks), 1)) * _IDF.get(t, 0) for t in tf}
    norm = math.sqrt(sum(x * x for x in q.values())) or 1.0
    q = {t: x / norm for t, x in q.items()}
    scored = []
    for i, dv in enumerate(_DOC_VECS):
        sim = sum(q.get(t, 0) * dv.get(t, 0) for t in q)
        scored.append((sim, i))
    scored.sort(reverse=True)
    return [{"score": round(s, 3), **CHUNKS[i]} for s, i in scored[:k] if s > 0]


def ask(client: anthropic.Anthropic, model: str, question: str, k: int = 4) -> dict:
    retrieved = retrieve(question, k)
    context = "\n\n".join(f'<document id="{c["id"]}">{c["text"]}</document>' for c in retrieved)
    prompt = f"""Answer using ONLY the documents below. If not in documents, say
"I don't know based on the provided sources."

{context}

Question: {question}

<answer>your answer citing sources like [chunk-N]</answer>
<citations><cite id="chunk-N"/></citations>"""
    resp = client.messages.create(model=model, max_tokens=800,
                                  messages=[{"role": "user", "content": prompt}])
    text = next((b.text for b in resp.content if b.type == "text"), "")
    answer_match = re.search(r"<answer>(.*?)</answer>", text, re.DOTALL)
    cite_matches = re.findall(r'<cite\s+id="([^"]+)"\s*/?>', text)
    return {
        "answer": (answer_match.group(1).strip() if answer_match else text.strip()),
        "citations": cite_matches,
        "retrieved": retrieved,
        "retrieved_ids": [c["id"] for c in retrieved],
        "raw": text,
    }
