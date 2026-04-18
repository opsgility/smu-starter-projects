# AI-103 Lesson 10 — Multi-agent + Approval + Tracing Starter

Scaffold for a multi-agent system with human-in-the-loop approval and OpenTelemetry tracing.

## Architecture

- **Orchestrator agent** — receives the user request, decides which worker(s) to call, drafts a plan
- **Refund worker** — handles refund requests; gated by an approval queue
- **Lookup worker** — handles read-only product/customer lookups; no approval required

## Files

- `app/orchestrator.py` — orchestrator agent + connected-agent tool wiring
- `app/worker.py` — worker agent factories (refund, lookup)
- `app/tracing.py` — OTel + Azure Monitor instrumentation
- `app/main.py` — FastAPI exposing `/request` and `/approvals`

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
az login
uvicorn app.main:app --reload --port 8000
```
