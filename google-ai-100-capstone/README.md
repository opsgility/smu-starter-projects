# google-ai-100-capstone

Starter for **Google AI 100 — Capstone: Merch-Desk Assistant**.

Build `nimbus-assist`: a CLI that, given a SKU (with a product photo and spec
PDF in Cloud Storage), emits a draft catalog entry, a one-sentence customer
summary, and three FAQ answers — all in validated JSON.

## Files

- `nimbus_assist.py` — CLI skeleton
- `sku_config.json` — sample SKU list with placeholder GCS URIs
- `schemas.py` — Pydantic schemas for catalog entry + FAQ bundle
- `requirements.txt`
- `FINDINGS.md` — blank file; record your model comparison observations

## During the capstone

You will upload 5 sample product photos + spec PDFs to
`${PROJECT_ID}-nimbus-skus/` in Cloud Storage (exact `gsutil` commands are in
the exercise) and point `sku_config.json` at those URIs.
