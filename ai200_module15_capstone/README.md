# ai200_module15_capstone — Northwind Logistics End-to-End

Starter project for **AI-200 Module 15**. Brings together Modules 2-14:

- Container image built with ACR (Module 2)
- Deployed to Container Apps (Module 4) with managed identity
- Cosmos vector store for RAG retrieval (Modules 6+7)
- Azure OpenAI for embeddings + chat
- Service Bus queue + Azure Functions consumer for async audit (Modules 10+12)
- Secrets via Key Vault, identity-based (Module 13)
- OpenTelemetry + Application Insights traces (Module 14)

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `app/main.py` | FastAPI `/ask` endpoint — TODOs in Steps 5 and 6 |
| `lib/cosmos_vector.py` | Cosmos vector search (complete) |
| `lib/embeddings.py` | Azure OpenAI embed + chat (complete) |
| `lib/secrets.py` | Key Vault helper (complete) |
| `lib/sb_producer.py` | Service Bus producer (complete) |
| `lib/telemetry.py` | OTel + Azure Monitor wiring (complete) |
| `functions/function_app.py` | Audit-writer Function (complete) |
| `scripts/seed.py` | Seeds 100 FAQs into incident_vectors |
| `scripts/ask_demo.py` | Drives sample questions through the live API |
| `Dockerfile` | Builds the FastAPI image |
