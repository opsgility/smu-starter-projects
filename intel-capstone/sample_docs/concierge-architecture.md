# SIB OSINT Concierge — Architecture Overview

The Concierge is one FastAPI service in front of one Azure AI Foundry
project. Four endpoints, one Application Insights trace stream.

## Endpoints

- `/health` — liveness probe.
- `/chat` — stateless analyst chat against the Responses API
  (`gpt-5`).
- `/rag` — hybrid + semantic search over the `sib-osint-kb` index,
  followed by a grounded Responses generation.
- `/agent` — Foundry AgentsClient 1.1 with two tools:
  `AzureAISearchTool` over `sib-osint-kb` and a custom FunctionTool
  named `_indicator_status` that looks up published feed entries.

## Foundry project

The `sib-osint-capstone` project owns:

- `gpt-5` deployment — chat and Responses.
- `text-embedding-3-large` deployment — 3072-dim embeddings used for
  RAG and search seeding.
- An Azure AI Search connection wired to the `sib-osint-kb` index.

## Observability

`app/tracing.py` calls `configure_azure_monitor()` at import time, so
every route is auto-instrumented. Each endpoint also opens a manual
parent span:

- `sib.chat.reply`
- `sib.rag.answer`
- `sib.agent.run`

Child spans for OpenAI, AI Search, and Agents calls are added by the
Azure SDK instrumentation.

## Authentication

`DefaultAzureCredential` is used by every client. In the lab, the
identity is the lab user's `az login` session. In a production
deployment the bureau would replace this with a workload-managed
identity.

## What's intentionally NOT in the Concierge

- Vision and image understanding — covered separately by the bureau's
  geospatial unit.
- Voice and speech — the Concierge is text-only.
- Document extraction — handled by the bureau's records-management
  pipeline.
