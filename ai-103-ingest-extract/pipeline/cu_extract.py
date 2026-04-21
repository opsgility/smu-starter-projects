"""Content Understanding analyzer helper for the Summitline Outfitters pipeline.

Exercise 1 (Lab 2273 / 3406) walks you through:
  * defining the `summitline-docs` analyzer schema (SCHEMA)
  * making `ensure_analyzer()` idempotent (GET -> short-circuit on 200, PUT on 404)
  * implementing the `Operation-Location` poll loop inside `extract()`

This module is imported by `pipeline.ingest` once the pipeline runs end-to-end.
"""
from __future__ import annotations

import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ENDPOINT = os.environ["CU_ENDPOINT"].rstrip("/")
KEY = os.environ["CU_KEY"]
API_VERSION = os.environ.get("CU_API_VERSION", "2024-12-01-preview")

ANALYZER_ID = "summitline-docs"

HEADERS = {
    "Ocp-Apim-Subscription-Key": KEY,
}

# ---------------------------------------------------------------------------
# Analyzer schema
# ---------------------------------------------------------------------------

# TODO (Exercise 1 Step 5): Replace this empty dict with the Summitline
# mixed-document field schema. The schema should set:
#   - description           : short human-readable string
#   - baseAnalyzerId        : "prebuilt-documentAnalyzer"
#   - config.returnDetails  : True
#   - fieldSchema.fields    : vendor, doc_type, total, invoice_date, summary
# Each field uses method="generate" so Content Understanding performs
# generative extraction (better for free-form descriptions than classic OCR).
SCHEMA: dict = {}


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------

def ensure_analyzer() -> None:
    """Create the analyzer if it does not already exist.

    GET first: if we get 200 back the analyzer already exists and we return.
    On 404 we PUT the schema. A 409 on PUT is treated as success (two
    workers racing to create the same analyzer).
    """
    # TODO (Exercise 1 Step 6): Implement the GET-then-PUT lifecycle.
    # 1. Build the analyzer URL from ENDPOINT, ANALYZER_ID, API_VERSION.
    # 2. GET the URL with HEADERS.
    # 3. If status_code == 200 -> return (already exists).
    # 4. If status_code != 404 -> raise_for_status() (unexpected error).
    # 5. Otherwise PUT SCHEMA as JSON. Accept 200/201/409 as success.
    raise NotImplementedError("Implement ensure_analyzer in Exercise 1 Step 6.")


# ---------------------------------------------------------------------------
# Extraction (long-running operation)
# ---------------------------------------------------------------------------

def extract(file_bytes: bytes) -> dict:
    """Run the analyzer over `file_bytes` and return markdown + fields.

    Returns a dict shaped like:
        {
            "markdown": "<markdown string>",
            "fields":   { "vendor": {...}, "doc_type": {...}, ... }
        }
    """
    # TODO (Exercise 1 Step 7): Implement the analyze+poll flow.
    # 1. POST to {ENDPOINT}/contentunderstanding/analyzers/{ANALYZER_ID}:analyze
    #    with api-version query param, Content-Type: application/octet-stream,
    #    and file_bytes as the body.
    # 2. Read the poll URL from r.headers["Operation-Location"]  (NOT "Location").
    # 3. Loop: GET the poll URL; inspect poll["status"].
    #      - "Succeeded" -> return {"markdown": ..., "fields": ...} from
    #        poll["result"]["contents"][0].
    #      - "Failed"    -> raise RuntimeError(poll).
    #      - otherwise   -> time.sleep(2) and poll again.
    raise NotImplementedError("Implement extract in Exercise 1 Step 7.")
