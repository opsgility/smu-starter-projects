# ai-901-capstone — Northwind Horizon Multimodal Assistant (FastAPI)

Capstone starter for AI-901 Obj 2 Part VIII. A FastAPI app with four routes:

- `POST /chat`       — Foundry chat completion (Obj 2 Part II).
- `POST /transcribe` — Azure Speech → text (Obj 2 Part V).
- `POST /vision`     — upload image → multimodal chat answer (Obj 2 Part VI).
- `POST /extract`    — upload document → Content Understanding fields (Obj 2 Part VII).

All four routes currently return `{"error": "not implemented"}`. The capstone has you wire each route using what you built in the earlier exercises.

## What's here
- `src/app.py` — FastAPI routes, all stubs.
- `src/foundry.py` — small helper that builds the Foundry clients (chat completions, agents, projects).
- `sample_data/` — one of each asset type for manual curl testing.

## Env vars
Copy `.env.example` → `.env` and fill in every variable — the capstone exercises all four modalities.

## Run
```
uvicorn src.app:app --reload --port 8000
curl -X POST http://localhost:8000/chat -d '{"message": "hi"}' -H "Content-Type: application/json"
```
