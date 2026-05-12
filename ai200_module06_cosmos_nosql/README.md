# ai200_module06_cosmos_nosql — Cosmos DB for NoSQL

Starter project for **AI-200 Module 6**. You will provision a Cosmos DB
account, ingest 5000 fake shipments, measure RU costs for an inefficient
query, apply a composite index, watch the RU drop an order of magnitude,
and compare Strong vs Session consistency read latency.

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `lib/cosmos_client.py` | Has a TODO in Step 4 — implement `get_client()` |
| `scripts/smoke_test_connection.py` | Verifies your Step 4 implementation |
| `scripts/seed.py` | Bulk-inserts 5000 shipments |
| `scripts/query_slow.py` | Runs the ORDER BY query and prints RU cost |
| `scripts/query_tuned.py` | Same query, run after composite index applied |
| `scripts/consistency_test.py` | 100-read latency probe |
| `indexing-policy.json` | Composite index definition you apply in Step 7 |

## Prerequisites

- Python 3.12+, Azure CLI 2.69+, pre-provisioned `rg-ai200-*` group
