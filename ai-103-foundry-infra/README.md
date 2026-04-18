# AI-103 Lesson 3 — Foundry Infrastructure Starter

Scaffold for creating a Foundry hub + project + supporting resources via Bicep, then wiring a GitHub Actions deploy workflow.

## Files

- `infra/main.bicep` — Foundry AI Services account, project, AI Search, Storage, Application Insights
- `infra/main.parameters.json` — parameters consumed by the deploy script
- `deploy.sh` — helper that runs `az deployment group create`
- `.github/workflows/deploy.yml` — GitHub Actions workflow using OIDC federated credentials

## Run

```bash
cp .env.example .env
az login
az group create --name <rg> --location eastus2
bash deploy.sh
```

## What you'll build

By the end of this lesson you'll have an end-to-end Foundry deployment plus a CI pipeline that redeploys on push to `main`.

## Environment

| Variable | Description |
|----------|-------------|
| `AZURE_SUBSCRIPTION_ID` | Target subscription |
| `AZURE_RESOURCE_GROUP`  | Pre-created resource group |
| `AZURE_LOCATION`        | Region (default: `eastus2`) |
| `PROJECT_NAME`          | Foundry project name |
| `HUB_NAME`              | Foundry hub resource name |
