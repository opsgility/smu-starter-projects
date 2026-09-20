# AI-300 Lesson 9 — Dispatcher Foundry Starter

Starter project for **AI-300 Lesson 9: Provision Meridian Dispatcher's Foundry stack + versioned prompts**.

## What's pre-provisioned by the lab

- **Azure AI Foundry account** with a **`dispatcher`** project
- Two model deployments under the `dispatcher` project:
  - `gpt-5.1` (chat)
  - `text-embedding-3-large` (embeddings)
- **Azure Container Apps environment** (empty — no app deployed yet)
- **Azure Container Registry** for the Dispatcher API image
- **Log Analytics workspace** + **Application Insights** for OpenTelemetry traces
- Federated-credential setup so the student can wire GitHub Actions OIDC into the pre-created identity

## What the student authors in this lab

1. A **versioned prompt** under `prompts/dispatcher_vN.md` (front-matter + system message body)
2. A **Dispatcher API** (`src/dispatcher_api.py`) — FastAPI + `azure-ai-projects` `AIProjectClient`, OTel-instrumented
3. A **prompt-promotion GitHub Actions workflow** that runs the candidate prompt through `gpt-5.1` against three golden dispatch scenarios on PR and posts the result as a PR comment
4. A **deploy workflow** that on push-to-`main` builds the container, pushes to ACR, and runs `az containerapp update` against the pre-provisioned Container Apps environment

## Layout

```
ai300_lesson9_dispatcher_foundry/
├── README.md                          # this file
├── .env.example                       # env vars the student fills in (Foundry endpoint, deployment names, ACR/ACA)
├── .gitignore
├── requirements.txt                   # azure-ai-projects, azure-identity, fastapi, uvicorn, OTel
├── Dockerfile                         # python:3.13-slim, uvicorn ASGI
├── prompts/
│   └── dispatcher_v1.md               # front-matter + Meridian dispatch system message
├── src/
│   ├── dispatcher_api.py              # FastAPI /dispatch endpoint, AIProjectClient, OTel
│   └── dispatcher_client.py           # local smoke-test client
├── data/
│   └── promote-scenarios.jsonl        # 3 golden dispatch scenarios for prompt promotion
└── .github/workflows/
    ├── promote-prompt.yml             # PR gate — runs candidate prompt against 3 scenarios, comments on PR
    └── deploy-dispatcher.yml          # push-to-main — build + push to ACR, deploy to Container Apps
```

## Local run

```bash
python -m venv .venv && source .venv/bin/activate    # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env                                  # fill in values from the lab environment
export $(grep -v '^#' .env | xargs)
uvicorn src.dispatcher_api:app --reload --port 8000
# in another terminal:
python src/dispatcher_client.py
```

## Auth

- **Local**: `DefaultAzureCredential` — `az login` on the lab VM; the pre-created identity has `Cognitive Services User` + `Cognitive Services OpenAI User` scoped to the Foundry account.
- **In Container Apps**: system-assigned managed identity of the container app — student wires this in Lesson 10, not here.
- **GitHub Actions**: OIDC to the pre-created federated identity credential; workflows use `azure/login@v2` with `client-id`/`tenant-id`/`subscription-id` from repo secrets.

## Model versions

- Chat: **gpt-5.1** (v2025-11-13). Current GA under GlobalStandard SKU.
- Embeddings: **text-embedding-3-large**.

Do not downgrade — the `promote-prompt.yml` scenario expectations are calibrated to gpt-5.1 output shape.
