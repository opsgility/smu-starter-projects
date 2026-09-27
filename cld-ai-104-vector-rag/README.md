# CLD-AI-104 Lesson 4 — Vector-search retriever

Second CLD-AI-104 hands-on. Build an embedding-based retriever using SentenceTransformers (`all-MiniLM-L6-v2`, ~80MB, pre-installed in the vscode-python-ai container). Compare recall against L2's TF-IDF baseline on 8 synonym-heavy queries.

If SentenceTransformers isn't available, the code falls back to a deterministic hash-based stub embedder — the pipeline shape is identical so students still learn the pattern; recall numbers just look flatter.

## Files

```
cld-ai-104-vector-rag/
  README.md, .env.example, .gitignore, requirements.txt
  data/knowledge_base.json    # Same 12 chunks as L2 (reproducible comparison).
  src/
    verify_env.py
    embedder.py               # COMPLETE: SentenceTransformers wrapper + stub fallback.
    vector_index.py           # Exercise 2 skeleton — TODO: build index + top-k search.
    compare_retrievers.py     # Exercise 3 — TF-IDF vs vector recall head-to-head.
```
