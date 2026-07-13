# AI-3016 Capstone — Sentinel Intelligence Bureau

End-to-end FastAPI app for the **Sentinel Intelligence Bureau (SIB)** OSINT
Modernization team. This is the capstone lab for the AI-3016 course; you take
the patterns learned in chat, tools, and RAG and wire them into one Foundry
project with one OpenTelemetry trace stream.

The capstone targets a **2-hour budget** and exposes four endpoints plus
health:

| Endpoint   | What it does                                                      | Touches                                              |
| ---------- | ----------------------------------------------------------------- | ---------------------------------------------------- |
| `/health`  | Liveness probe                                                    | —                                                    |
| `/chat`    | Stateless analyst chat                                            | AIProjectClient → OpenAI Responses (gpt-5)           |
| `/rag`     | Grounded answer with citations from `sib-osint-kb`                | Embeddings + Azure AI Search hybrid/semantic         |
| `/agent`   | Tool-using concierge (indicator lookup + KB search)               | AgentsClient 1.1.0, FunctionTool, AzureAISearchTool  |

Everything is observable in the Application Insights component deployed by
the lab's ARM template.

## Layout

```
intel-capstone/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app — wires every endpoint (complete)
│   ├── tracing.py       # configure_azure_monitor() — Exercise 1
│   ├── chat.py          # /chat — Exercise 1
│   ├── rag.py           # /rag — Exercise 1
│   └── agent.py         # /agent — Exercise 2
├── sample_docs/         # SIB OSINT handbook + policies (seeded into search)
├── seed_index.py        # Upload sample_docs/ into the sib-osint-kb search index
├── test_client.py       # Exercise 3 smoke test — hits every endpoint
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Scenario

You are a Senior AI Engineer on SIB's **OSINT Modernization** team. The
Concierge needs one platform that can:

1. Answer analyst questions about handbook and policy (`/chat`).
2. Ground policy answers in the real KB so the assistant never invents a
   collection rule (`/rag`).
3. Look up published threat-feed indicators via a tool call, and pivot to
   KB search for anything else (`/agent`).

The capstone proves you can build all three on one Azure AI Foundry project
with one OTel trace stream feeding Application Insights.

All sample data is non-classified, fictional, and synthesized for training.

## Prerequisites

The lab's ARM template pre-deploys everything for you:

- Azure AI Foundry account (kind `AIServices`) with `gpt-5` +
  `text-embedding-3-large` deployments
- Foundry project (the `projectEndpoint` for AIProjectClient / AgentsClient)
- Azure AI Search (Basic, semantic free, vector-enabled)
- Storage account with `sib-osint-docs` container
- Log Analytics workspace + workspace-based Application Insights
- Role assignments for your lab identity (completed in Exercise 1 Step 4)

Local tools are already installed in the VS Code Server lab image:
Python 3.11+, `az` CLI (already logged in as the lab user).

## Setup

The workspace is already the starter root; no `cd` needed.

```bash
# Copy the example env file and let Exercise 1 Step 3 append real deployment values.
cp .env.example .env

# Install dependencies (the lab image already has them, but this is safe to re-run).
pip install -r requirements.txt
```

## One-time search-index seed

After Exercise 1 creates the `sib-osint-kb` index schema, seed it with the
bundled docs:

```bash
python seed_index.py
```

Output: `Uploaded N documents to sib-osint-kb`.

## Run the app

```bash
set -a; source .env; set +a
uvicorn app.main:app --reload --port 8000
```

Leave that terminal running. Open a second terminal for smoke tests:

```bash
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/chat -F "message=Summarize the Concierge's role."
python test_client.py
```

## Observability

Every request becomes one distributed trace in the lab's Application
Insights component (`sib-osint-appi-<suffix>`). Portal → Transaction
search shows spans named `/chat`, `/rag`, `/agent`, each with nested
OpenAI / Search / Agents child spans.

The key is that `app/tracing.py` calls `configure_azure_monitor()`
**at import time** — before `app = FastAPI()` instantiates. Instrumenting
after the app object would leave early routes dark.

## Troubleshooting

See the Troubleshooting section of each exercise and the lab's own
guidance. The most common failures:

- `ValueError: A connection string must be supplied` — `.env` not sourced;
  `set -a; source .env; set +a`.
- `ClientAuthenticationError` — `az login` missing or wrong subscription.
- `ToolHandlerNotFound` on `/agent` — `enable_auto_function_calls(toolset)`
  missing or called after `create_and_process`.
- `AuthorizationPermissionMismatch` on Search — role propagation. Wait 2–5
  minutes.
- `/rag` returns empty `sources` — index empty; run `python seed_index.py`.
