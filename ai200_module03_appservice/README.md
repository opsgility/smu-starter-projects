# ai200_module03_appservice — Deploy Containerized AI APIs to Azure App Service

Starter project for **AI-200 Module 3**. The shipment-classifier from Module 2 is
extended with `/healthz` and `/secrets-check` endpoints. In the lab you create an
App Service Plan, deploy a Web App for Containers pointing at the ACR image,
wire Key Vault references into App Settings, and validate the live endpoint.

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `app/main.py` | FastAPI app with `/`, `/healthz`, `/classify`, `/secrets-check` |
| `requirements.txt` | Pinned versions |
| `Dockerfile` | Same base image as Module 2; exposes `PORT=8000` + `WEBSITES_PORT=8000` |
| `scripts/verify.sh` | Hits all three endpoints against `$APP_URL` |
| `.env.example` | Variables you'll populate |

## What you will build

- A Standard-tier Linux App Service Plan
- A Web App for Containers running the Module-2 image **by digest**
- A system-assigned managed identity with `AcrPull` on the registry
- Three App Settings backed by Key Vault references (no plaintext secrets)
- A `curl` against the live FQDN that returns `200 OK` from all three routes

## Prerequisites

- Python 3.12+
- Azure CLI 2.69+
- A completed Module 2 (so the ACR has a `shipment-classifier:1.0.0` image)
