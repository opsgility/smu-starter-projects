"""Content Understanding wrapper for /extract-document."""
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["CU_ENDPOINT"].rstrip("/")
KEY = os.environ["CU_KEY"]
API_VERSION = os.environ.get("CU_API_VERSION", "2024-12-01-preview")
ANALYZER_ID = "ai901-capstone-invoice"

HEADERS = {"Ocp-Apim-Subscription-Key": KEY}


def extract(pdf_path: Path) -> dict:
    # TODO 1: ensure the "ai901-capstone-invoice" analyzer exists (PUT analyzers/{id}?api-version=...).
    # TODO 2: POST the file bytes to analyzers/{id}:analyze and grab Operation-Location header.
    # TODO 3: poll the operation URL until "Succeeded", return result["result"]["contents"][0]["fields"].
    raise NotImplementedError
