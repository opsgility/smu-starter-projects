# AI-103 Lesson 2 — Model Explorer Starter

Scaffold for comparing Foundry-deployed models side-by-side. You'll deploy 3-4 models and use these scripts to measure latency, token cost, and tool-calling capability.

## Files

- `compare_models.py` — run the same prompt against every deployment, print latency + usage table
- `toolcall_probe.py` — send a tool-calling probe to each deployment, report which ones called the tool

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
az login
python compare_models.py "Summarize Azure AI Foundry in one sentence."
python toolcall_probe.py
```

## Environment

| Variable | Description |
|----------|-------------|
| `AZURE_AI_PROJECT_ENDPOINT` | Foundry project endpoint (from the Foundry portal's "Libraries" pane) |
| `MODEL_DEPLOYMENTS` | Comma-separated list of deployment names |
