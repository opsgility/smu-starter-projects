# AI-103 Lesson 4 — Keyless Auth Migration Starter

Scaffold that starts with API key authentication and asks you to migrate to Entra ID + managed identity, following the AI-103 security guidance.

## Files

- `app/main.py` — FastAPI chat endpoint. Starts using `AZURE_OPENAI_API_KEY`.
- `bicep/identity.bicep` — user-assigned managed identity + role assignment. **You'll fill this in.**

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill AZURE_OPENAI_* to match your deployment
uvicorn app.main:app --reload --port 8000
curl -X POST http://127.0.0.1:8000/chat -d "message=hello"
```

## What you'll do

1. Verify the key-based version works (step 0 of the exercise).
2. Replace the API key client with a `DefaultAzureCredential`-backed one using `AIProjectClient.get_openai_client()`.
3. Author `bicep/identity.bicep` to create a user-assigned managed identity + `Azure AI User` role assignment on the Foundry project scope.
4. Re-run against the Foundry endpoint (no secrets in `.env`).
