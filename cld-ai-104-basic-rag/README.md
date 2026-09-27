# CLD-AI-104 Lesson 2 — Basic retrieve-and-generate RAG pipeline

First CLD-AI-104 hands-on. Build a working RAG pipeline over an Orion Analytics knowledge base (SLA runbook, refund policy, product docs, compliance memos) using a tiny in-process TF-IDF retriever + Claude for generation with cited answers.

Uses Python stdlib TF-IDF (no external embedding model dependency) so students focus on RAG mechanics; L4 covers real embedding-based vector search.

## Files

```
cld-ai-104-basic-rag/
  README.md, .env.example, .gitignore, requirements.txt
  data/knowledge_base.json    # 12 short chunks from 4 doc sources
  src/
    verify_env.py
    retriever.py              # COMPLETE: TF-IDF over the corpus.
    rag.py                    # Exercise 2 skeleton — TODO: compose prompt, call Claude, parse citations.
    ask.py                    # Exercise 3 script — 8 questions, verifies expected chunks were retrieved.
```
