# ai-901-responsible-ai — Content Safety scaffold

Starter for AI-901 Obj 1 Part I (Responsible AI Principles). You will use Azure AI Content Safety to score sample prompts for harm categories (hate, sexual, violence, self-harm) and detect jailbreak attempts. The exercise has you wire this into a "Responsible AI gate" function.

## What's here
- `src/main.py` — loads `sample_data/prompts.json`, calls `ContentSafetyClient.analyze_text()`, prints category/severity per prompt. The `run_rai_gate()` function is intentionally left with a `TODO` — the exercise has you implement the block/allow logic.
- `sample_data/prompts.json` — 5 short prompts: benign, mildly unsafe, clearly unsafe, jailbreak attempt, PII leak.
- `requirements.txt` — `azure-ai-contentsafety`, `azure-identity`, `python-dotenv`.

## Env vars
Copy `.env.example` → `.env` and fill in:
- `CONTENT_SAFETY_ENDPOINT` — your Azure AI Content Safety endpoint (Foundry portal → your Content Safety / AI Services resource → **Keys and Endpoint**).

Auth uses `DefaultAzureCredential` — no key is required; the exercise signs you in with `az login`.

## Run
```
python src/main.py
```
You should see a table of prompt → category scores. Any row with severity ≥ 2 is a candidate for blocking — wiring the block logic is the exercise.
