# ai200_module07_cosmos_vector — Cosmos DB Vector Search + Change Feed

Starter project for **AI-200 Module 7**. You enable Cosmos vector search on
a fresh container, seed source documents into a sibling container, and use
the change feed to embed-and-store as new documents arrive.

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `lib/cosmos_client.py` | Complete (lifted from Module 6) |
| `lib/embeddings.py` | Azure OpenAI embeddings wrapper |
| `lib/vector_store.py` | TODOs in `upsert_vector` (Step 6a) and `search_similar` (Step 6b) |
| `lib/change_feed.py` | TODO in `on_new_incident` (Step 8) |
| `scripts/seed_incidents.py` | Seeds 210 source incidents |
| `scripts/changefeed_processor.py` | Runs the change feed processor once |
| `scripts/search.py` | Free-text vector search CLI |
| `scripts/smoke_test.py` | Runs after Step 6 to confirm vector wiring works |
| `vector-policy.json` | Vector embedding policy applied at container creation |
| `vector-indexing-policy.json` | Indexing policy enabling DiskANN on `/embedding` |

## Prerequisites

- Module 6 was completed (Cosmos account + `northwind` database exist)
- Azure OpenAI deployment for `text-embedding-3-small` (the lab provisions it)
