# AI-103 Lesson 6 — Chat + Tool Calling Starter

Scaffold for a FastAPI streaming chat endpoint that supports three function tools:
- `get_weather(city)` — mocked weather
- `calculate(expr)` — safe arithmetic
- `lookup_inventory(sku)` — sample Northwind catalog

## Files

- `app/main.py` — FastAPI app with `/chat` and `/stream` endpoints
- `app/tools.py` — tool definitions + Python implementations
- `test_client.py` — quick smoke test hitting `/chat` and `/stream`

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
az login
uvicorn app.main:app --reload --port 8000
python test_client.py
```
