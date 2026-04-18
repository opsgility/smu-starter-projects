"""Content Understanding analyzer wrapper exposed as an agent function tool."""
import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["CU_ENDPOINT"].rstrip("/")
KEY = os.environ["CU_KEY"]
API_VERSION = os.environ.get("CU_API_VERSION", "2024-12-01-preview")
ANALYZER_ID = "ai103-knowledge-invoice"
HEADERS = {"Ocp-Apim-Subscription-Key": KEY}


def extract_invoice(file_path: str) -> str:
    """Extract structured fields from an invoice PDF.

    :param file_path: Absolute path to a PDF invoice.
    :return: JSON string of extracted fields (vendor, total, items, etc.).
    """
    pdf = Path(file_path)
    # TODO 1: PUT analyzers/{ANALYZER_ID}?api-version=... with a body that defines the
    #         invoice analyzer (use the schema from the AI-901 lesson 10 starter as a
    #         reference and tighten fields for invoices).
    # TODO 2: POST analyzers/{ANALYZER_ID}:analyze with the PDF bytes;
    #         capture the Operation-Location header.
    # TODO 3: Poll Operation-Location until status == "Succeeded" then return
    #         json.dumps(result["result"]["contents"][0]["fields"]).
    raise NotImplementedError
