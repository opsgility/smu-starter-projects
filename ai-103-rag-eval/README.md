# AI-103 Lesson 7 — RAG + Evaluation Starter

Scaffold for a RAG application grounded on Azure AI Search, with Foundry evaluations.

## Files

- `app/retrieval.py` — index creation + chunking + ingestion + hybrid retrieval
- `app/main.py` — FastAPI `/chat` endpoint that retrieves grounding then asks the model
- `app/evaluate.py` — runs `evaluate()` on a sample dataset
- `sample_docs/` — markdown docs to ingest
- `eval_data.jsonl` — golden Q/A pairs

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
az login
python -m app.retrieval ingest          # build index + load docs
uvicorn app.main:app --reload --port 8000
python -m app.evaluate
```
