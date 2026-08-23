# AI-500 Lesson 18 — Ship Ridgevault to production via DTAP, canary rollout, and CI/CD

Capstone starter for the AI-500 course. In this lab you take the multi-agent portfolio-review system you built in Lessons 3–17 (Ridgevault Financial's automated investment-review pipeline) and put it through a real release process: containerize it, deploy through Dev → Test → Acceptance → Production on Azure Container Apps, wire a GitHub Actions CI/CD pipeline, run a canary revision at 10% traffic, and prove you can roll back a bad deploy in under two minutes.

## Scenario

Ridgevault Financial's compliance officer just approved the multi-agent portfolio-review system for production use. Legal wants a controlled release with a documented rollback path, ops wants a canary before 100% traffic, and Ridgevault's platform team wants the whole thing shipped by CI/CD instead of a laptop. Your job: take the L3–L17 codebase and ship it through DTAP with a canary and a working rollback.

## Files

```
ai-500-capstone/
  README.md                        Scenario, files, run instructions.
  .env.example                     Foundry endpoint + model + Container Apps outputs.
  .gitignore                       Excludes .env, __pycache__, .venv.
  requirements.txt                 Reference manifest — every listed package is preinstalled in the python-ai container variant.
  Dockerfile                       Small python:3.11-slim image running FastAPI + uvicorn.
  azure.yaml                       azd project manifest (name, services, hooks).
  src/
    verify_env.py                  Smoke test — reads .env, does one Foundry chat round-trip.
    portfolio_flow.py              FastAPI app that wraps the L3-L17 portfolio-review multi-agent flow.
    agents/
      __init__.py
      intake_agent.py              Stub for the L3 intake agent (customer profile parser).
      risk_agent.py                Stub for the L7 risk-scoring agent.
      recommendation_agent.py      Stub for the L11 recommendation composer + L11 evaluation harness hook.
  infra/
    main.bicep                     Deployment manifest for azd (references the platform ARM template outputs).
  .github/
    workflows/
      deploy.yml                   GitHub Actions workflow — build image, push to ACR, deploy revision, run smoke test.
  scripts/
    canary_split.sh                az containerapp ingress traffic set — 90/10 split.
    rollback.sh                    Revert traffic to the last-known-good revision.
```

## How to run

The lab's ARM template pre-provisions the Foundry account, project, gpt-5 deployment, Container Apps environment, Container Registry, and App Insights before you land in VS Code. Everything you need is already in your environment.

1. Sign in to Azure inside the VS Code terminal:
   ```bash
   az login --use-device-code
   ```
   Open `https://microsoft.com/devicelogin` in a new browser tab and paste the code the CLI shows.
2. Copy the values from the lab's Environment tab into `.env`:
   ```bash
   cp .env.example .env
   # edit .env — paste FOUNDRY_PROJECT_ENDPOINT, FOUNDRY_MODEL, CONTAINER_APP_NAME,
   # CONTAINER_APP_ENV, ACR_LOGIN_SERVER, APPLICATIONINSIGHTS_CONNECTION_STRING
   ```
3. Confirm auth + Foundry connectivity:
   ```bash
   python src/verify_env.py
   ```
4. Follow the lab exercises in the right pane. Each exercise walks you through one DTAP stage.

## Authentication

The lab credential is `azureaiuser` — a Foundry User + Cognitive Services User + Contributor + Search / Blob data roles at subscription scope. No API keys. Every call in `portfolio_flow.py` uses `DefaultAzureCredential()`, which picks up your `az login --use-device-code` session automatically.

## Notes

- The container image referenced from `deploy.yml` is `<acr>.azurecr.io/portfolio-flow:<sha>` — the workflow builds and pushes it fresh on every merge.
- Canary weights: 90/10 is the default in `scripts/canary_split.sh`. Adjust the arguments to try other splits.
- Rollback restores 100% traffic to whichever revision was serving before the current one — read `rollback.sh` and confirm the target revision name before running in production for real.
- Nothing here is hardcoded to a model version — every AI call reads `FOUNDRY_MODEL` from the environment. Bump the value in `.env` and redeploy to try a different model.
