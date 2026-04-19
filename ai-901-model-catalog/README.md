# ai-901-model-catalog — Foundry model catalog browser

Starter for AI-901 Obj 1 Part II (AI Models & Configurations). Lists the deployments in your Foundry project and walks through the model catalog programmatically. The exercise has you deploy a chat model, then extend this starter to filter deployments by SKU.

## What's here
- `src/list_models.py` — uses `AIProjectClient.deployments.list()` to print deployment name, model name, type, SKU.
- `src/deploy_model.py` — stub for creating a deployment (exercise walks you through the portal path first, then you fill in the SDK equivalent).
- `requirements.txt` — `azure-ai-projects`, `azure-identity`, `python-dotenv`.

## Env vars
Copy `.env.example` → `.env` and fill in:
- `FOUNDRY_PROJECT_ENDPOINT` — Foundry portal → **Project → Overview → Project endpoint** (full URL ending in `.../api/projects/<project-name>`).
- `MODEL_DEPLOYMENT_NAME` — the deployment you'll create in the exercise (default: `gpt-4o-mini`).

Auth: `DefaultAzureCredential` — the lab signs you in with `az login`.

## Run
```
python src/list_models.py
```
On a fresh project this prints "no deployments yet" — creating the first one is the exercise.
