# AI-103 Lesson 13 — Ingest + Extract Pipeline Starter

End-to-end pipeline: source PDFs/images → Content Understanding for field extraction → chunking + embedding → Azure AI Search index. Then a query script demonstrates hybrid retrieval over the result.

## Files

- `pipeline/ingest.py`     — pulls files from blob storage and orchestrates the pipeline
- `pipeline/cu_extract.py` — Content Understanding analyzer creation + extraction
- `pipeline/index.py`      — index schema + upload
- `pipeline/query.py`      — sample hybrid query
- `sample_data/`           — drop sample PDFs here (invoices, contracts, statements)

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
az login
az storage blob upload-batch --account-name <acct> --destination ai103-source --source ./sample_data
python -m pipeline.ingest
python -m pipeline.query "What is the total of invoice INV-9001?"
```
