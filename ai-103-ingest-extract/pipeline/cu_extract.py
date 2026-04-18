"""Content Understanding analyzer ensure + extract."""
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["CU_ENDPOINT"].rstrip("/")
KEY = os.environ["CU_KEY"]
API_VERSION = os.environ.get("CU_API_VERSION", "2024-12-01-preview")
ANALYZER_ID = "ai103-extracted-doc"
HEADERS = {"Ocp-Apim-Subscription-Key": KEY}


def ensure_analyzer() -> None:
    """Idempotent: PUT the analyzer if it doesn't exist."""
    # TODO 1: GET {ENDPOINT}/contentunderstanding/analyzers/{ANALYZER_ID}?api-version=...
    #         If 200, return. If 404, PUT with a generic schema (vendor, doc_type, total,
    #         summary, fields[]). Raise on other errors.
    raise NotImplementedError


def extract(file_bytes: bytes) -> dict:
    """Run analysis on bytes; poll Operation-Location; return the extracted markdown +
    structured fields."""
    # TODO 2: POST {ENDPOINT}/contentunderstanding/analyzers/{ANALYZER_ID}:analyze?api-version=...
    #         with body=file_bytes; Content-Type: application/octet-stream.
    # TODO 3: Poll the Operation-Location header until status == "Succeeded";
    #         return {"markdown": result["result"]["contents"][0]["markdown"],
    #                 "fields": result["result"]["contents"][0]["fields"]}.
    raise NotImplementedError
