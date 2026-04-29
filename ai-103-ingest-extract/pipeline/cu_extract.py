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

# Exercise 1 - Step 5 Start
SCHEMA: dict = {}
# Exercise 1 - Step 5 End


# ---------------------------------------------------------------------------
# Lifecycle
# ---------------------------------------------------------------------------

def ensure_analyzer() -> None:
    """Create the analyzer if it does not already exist.

    GET first: if we get 200 back the analyzer already exists and we return.
    On 404 we PUT the schema. A 409 on PUT is treated as success (two
    workers racing to create the same analyzer).
    """
    # Exercise 1 - Step 6 Start
    raise NotImplementedError("Complete Exercise 1 Step 6")
    # Exercise 1 - Step 6 End


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
    # Exercise 1 - Step 7 Start
    raise NotImplementedError("Complete Exercise 1 Step 7")
    # Exercise 1 - Step 7 End
