# AI-901 Lesson 2 — Foundry Model Catalog & Deployment Starter

Scaffold for the Lesson 2 lab exercises. You'll browse the Microsoft Foundry model catalog, compare models by capability, and deploy a model via the Foundry SDK.

## Setup

```bash
pip install -r requirements.txt
az login
cp .env.example .env   # fill in PROJECT_ENDPOINT
```

## Files

- `list_models.py` — list and filter models in the Foundry catalog
- `deploy_model.py` — deploy a selected model to your project
- `inspect_config.py` — print deployment configuration parameters
