# AI-103 Capstone — Summitline Outfitters

End-to-end FastAPI app for Summitline Outfitters, the outdoor-gear retailer you've worked with throughout AI-103. Six endpoints, one OTel trace stream, one Azure AI Foundry account.

| Endpoint        | What it does                                          | Touches                                          |
| --------------- | ----------------------------------------------------- | ------------------------------------------------ |
| `/health`       | Liveness probe                                        | —                                                |
| `/chat`         | Stateless product / policy chat                       | AIProjectClient -> OpenAI Responses (gpt-4.1)    |
| `/rag`          | Grounded answer with citations                        | Embeddings + Azure AI Search hybrid/semantic     |
| `/agent`        | Tool-using concierge (order lookup + KB search)       | AgentsClient 1.1.0, FunctionTool, AzureAISearch  |
| `/vision-ask`   | Answer questions about an uploaded image              | Responses API `input_image` content              |
| `/extract-doc`  | Extract `vendor`/`doc_type`/`total` from a PDF        | Azure AI Content Understanding (REST)            |
| `/voice`        | Audio-in -> chat -> audio-out                         | Speech SDK STT + TTS around `chat.reply`         |

Everything is observable in the Application Insights component deployed by the lab's ARM template.

## Layout

```
ai-103-capstone/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app — wires every endpoint (complete)
│   ├── tracing.py       # configure_azure_monitor() — Exercise 1
│   ├── chat.py          # /chat — Exercise 1
│   ├── rag.py           # /rag — Exercise 1
│   ├── agent.py         # /agent — Exercise 2
│   ├── vision.py        # /vision-ask — Exercise 2
│   ├── cu.py            # /extract-doc (Content Understanding) — Exercise 3
│   └── speech.py        # /voice (Speech SDK) — Exercise 3
├── sample_docs/         # Summitline product + policy markdown (seeded into search)
├── sample_data/         # Placeholder storefront.jpg / invoice.pdf for manual testing
├── seed_index.py        # Upload sample_docs/ into the summitline-kb search index
├── test_client.py       # Exercise 4 smoke test — hits every endpoint
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Scenario

**Summitline Outfitters** is a mid-size outdoor-gear retailer. Their AI team needs one platform that can:

1. Answer product questions from the website (`/chat`).
2. Ground policy answers in the real KB so the bot never hallucinates return windows (`/rag`).
3. Look up real order status via a tool call, and pivot to KB search for anything else (`/agent`).
4. Accept photos from support tickets — damaged gear, storefront signage, receipts (`/vision-ask`).
5. Extract structured fields from vendor invoices nightly (`/extract-doc`).
6. Power in-store voice kiosks (`/voice`).

The capstone proves you can build all six on one Azure AI Foundry project with one OTel trace stream feeding Application Insights.

## Prerequisites

The lab's ARM template pre-deploys everything for you:

- Azure AI Foundry account (kind `AIServices`) with `gpt-4.1` + `text-embedding-3-large` deployments
- Foundry project (the `projectEndpoint` for AIProjectClient / AgentsClient)
- Azure AI Search (Basic, semantic free, vector-enabled)
- Storage account with `summitline-docs` container
- Log Analytics workspace + workspace-based Application Insights
- Role assignments for your lab identity (completed in Exercise 1 Step 4)

Local tools you need (already installed in the VS Code Server lab image):

- Python 3.11+
- `az` CLI, logged in as the lab user (`az login`)

## Setup

```bash
cd ai-103-capstone

# Copy the example env file and let Exercise 1 Step 3 append real deployment values.
cp .env.example .env

# Install dependencies (the lab image already has them, but this is safe to re-run).
pip install -r requirements.txt
```

## One-time search-index seed

After Exercise 1 creates the `summitline-kb` index schema, seed it with the bundled docs:

```bash
python seed_index.py
```

Output: `Uploaded N documents to summitline-kb`.

## Run the app

```bash
set -a; source .env; set +a
uvicorn app.main:app --reload --port 8000
```

Leave that terminal running. Open a second terminal for smoke tests:

```bash
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/chat -F "message=Recommend a daypack under 150 dollars."
python test_client.py
```

## Observability

Every request becomes one distributed trace in the lab's Application Insights component (`summitline-appi-<suffix>`). Portal -> Transaction search shows spans named `/chat`, `/rag`, `/agent`, `/vision-ask`, `/extract-doc`, `/voice`, each with nested OpenAI / Search / CognitiveServices child spans.

The key is that `app/tracing.py` calls `configure_azure_monitor()` **at import time** — before `app = FastAPI()` instantiates. Instrumenting after the app object would leave early routes dark.

## Troubleshooting

See the Troubleshooting section of each exercise and the lab's own guidance. The most common failures:

- `ValueError: A connection string must be supplied` — `.env` not sourced; `set -a; source .env; set +a`.
- `ClientAuthenticationError` — `az login` missing or wrong subscription.
- `ToolHandlerNotFound` on `/agent` — `enable_auto_function_calls(toolset)` missing or called after `create_and_process`.
- `AuthorizationPermissionMismatch` on Search — role propagation. Wait 2–5 minutes.
- `/rag` returns empty `sources` — index empty; run `python seed_index.py`.
