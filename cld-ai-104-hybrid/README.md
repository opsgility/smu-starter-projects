# CLD-AI-104 Lesson 8 — Hybrid search + reranker

Fourth CLD-AI-104 hands-on. Build a hybrid retriever (BM25 + vector) with Reciprocal Rank Fusion, then add a stub reranker layer. Compare P@5 across TF-IDF, vector, hybrid, and hybrid+rerank.

## Files
```
cld-ai-104-hybrid/
  README.md, .env.example, .gitignore, requirements.txt
  data/knowledge_base.json     # 12 chunks
  data/queries.json            # 10 queries mixing natural-language + exact-term
  src/
    verify_env.py
    hybrid.py                  # Exercise 2 — TODO: BM25 + vec + RRF + rerank
    compare_all.py             # Exercise 3 — 4-lane P@5 comparison
```
