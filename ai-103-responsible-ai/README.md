# AI-103 Lesson 5 — Responsible AI Starter

Scaffold for applying responsible AI controls to a generative app. You'll wire:
- Pre-filter (Content Safety)
- Post-filter (Content Safety)
- Quality + safety evaluation (Foundry evaluators)
- Approval gate (human-in-the-loop)

## Files

- `app/filters.py` — Content Safety wrapper for pre/post checks
- `app/evals.py` — Foundry `evaluate()` runner (groundedness, relevance, violence, hate)
- `app/approval.py` — simple approval queue (dict-backed)
- `app/main.py` — FastAPI orchestrator
- `eval_data.jsonl` — sample Q/A pairs for evaluation

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
az login
uvicorn app.main:app --reload --port 8000
python -m app.evals        # run evaluations against eval_data.jsonl
```
