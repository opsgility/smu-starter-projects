# ai200_module08_pgvector — Postgres + pgvector for RAG

Starter project for **AI-200 Module 8**. You provision an Azure Postgres
Flexible Server, install the `vector` extension, build a `docs` table with
a 1536-dim `vector` column + GIN-indexed `JSONB` metadata, ingest 200
seed docs with Azure OpenAI embeddings, then run filtered RAG retrievals.

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `lib/pg.py` | `get_conn()` has a TODO — Step 4 |
| `lib/embeddings.py` | Azure OpenAI wrapper (complete) |
| `lib/rag.py` | `upsert_doc` (Step 6a) and `search_with_filter` (Step 6b) TODOs |
| `db/migrations/001_extension.sql` | `CREATE EXTENSION vector` |
| `db/migrations/002_docs_table.sql` | docs table + B-tree/GIN indexes |
| `db/migrations/003_hnsw_index.sql` | HNSW cosine ANN index (applied AFTER ingest) |
| `scripts/migrate.py` | Applies all migrations in order |
| `scripts/seed.py` | Inserts 200 KB docs with embeddings |
| `scripts/search.py` | Filtered RAG query CLI |
| `scripts/smoke_test.py` | Confirms Step 4 + Step 6 work |
