# Retrieval-Augmented Generation (RAG)

RAG combines a search step with a generation step. Instead of asking a model to answer
from its parametric memory, the application first retrieves relevant passages from a
vector or hybrid index, then passes them to the model as grounding context.

## Why RAG

- **Freshness** — the model can answer over data updated after its training cutoff.
- **Provenance** — the application can cite the source of every claim.
- **Cost** — smaller models can perform well when given the right context.
- **Safety** — fabrications are reduced because the model is told to answer only from
  the supplied context.

## Hybrid search

In Azure AI Search, a hybrid query combines BM25 keyword scoring with vector similarity
in a single request. Submitting both `search_text` and `vector_queries` causes the
service to merge results using Reciprocal Rank Fusion (RRF). Adding a semantic ranker
on top further improves precision for natural-language queries.
