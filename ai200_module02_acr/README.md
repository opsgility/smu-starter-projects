# ai200_module02_acr — Build, Tag & Push with Azure Container Registry

Starter project for **AI-200 Module 2**. The Northwind shipment-classifier FastAPI
service is already implemented; your job in the lab is to build it into a
container image, push it to ACR via `az acr build`, capture the immutable
digest, and verify the image round-trips back from the registry.

## What's already scaffolded

| Path | Purpose |
| --- | --- |
| `app/main.py` | FastAPI app exposing `GET /`, `GET /healthz`, `POST /classify` |
| `requirements.txt` | Pinned FastAPI / uvicorn / pydantic versions |
| `Dockerfile` | Multi-stage build on `mcr.microsoft.com/azurelinux/base/python:3.12` |
| `acr-task.yaml` | Multi-step ACR Task (build → smoke-test → push) used by the local-context task run |
| `rules.json` | Classifier rule table — pushed as an OCI artifact alongside the image |
| `.dockerignore` / `.gitignore` | Hygiene |
| `.env.example` | Variables you'll populate during the lab |

## What you will build

- An ACR repository named `shipment-classifier` with tags `1.0.0` and `latest`
- An immutable `sha256:` digest reference that later modules pull by digest
- (Optional) A commit-triggered ACR Task pointing at this repo's `main` branch

## Prerequisites

- Python 3.12+
- Azure CLI 2.69+ (`az version`)
- Your VS Code lab container (pre-provisioned with both)

## Local smoke test (optional)

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
curl -s -X POST http://localhost:8000/classify \
  -H 'content-type: application/json' \
  -d '{"shipment_id":"ship-001","description":"package soaked from rain"}'
```

Expected output:

```json
{"shipment_id":"ship-001","label":"water-damage"}
```

## Following modules

- Module 3 (App Service) pulls the same image by digest into a Web App for Containers.
- Module 4 (Container Apps) reuses the same image with KEDA scaling.
- Module 5 (AKS) reuses the same image in a Deployment manifest.
