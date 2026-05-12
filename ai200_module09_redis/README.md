# ai200_module09_redis — Azure Managed Redis (Cache + Vector Index)

Starter project for **AI-200 Module 9**. You provision an Azure Managed Redis
instance, then exercise two patterns: a cache-aside wrapper for OpenAI chat
completions, and a RediSearch HNSW cosine index for vector retrieval.

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `lib/redis_client.py` | `get_redis` TODO (Step 4) |
| `lib/cache.py` | `cached_call` TODO (Step 6) |
| `lib/vector_index.py` | `upsert_doc` (Step 8a), `knn_search` (Step 8b) TODOs; `create_index` complete |
| `lib/embeddings.py` | Azure OpenAI embeddings + chat |
| `scripts/cache_demo.py` | Calls `cached_call` twice — second hits |
| `scripts/seed_vectors.py` | Seeds 104 KB docs |
| `scripts/vector_search.py` | KNN search CLI |
| `scripts/smoke_test.py` | Sanity-checks everything |
