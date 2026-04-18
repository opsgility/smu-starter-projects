"""Capstone Content Understanding wrapper."""
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["CU_ENDPOINT"].rstrip("/")
KEY = os.environ["CU_KEY"]
API_VERSION = os.environ.get("CU_API_VERSION", "2024-12-01-preview")
ANALYZER_ID = "ai103-capstone-doc"
HEADERS = {"Ocp-Apim-Subscription-Key": KEY}


def extract(file_bytes: bytes) -> dict:
    # TODO 1: ensure analyzer (PUT analyzers/{id}?api-version=...).
    # TODO 2: POST analyzers/{id}:analyze with bytes; capture Operation-Location.
    # TODO 3: poll until Succeeded; return result["result"]["contents"][0]["fields"].
    raise NotImplementedError
