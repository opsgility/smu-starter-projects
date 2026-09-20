"""Exercise 3 — Azure AI Content Understanding visual analyzer.

Implements a typed field-schema analyzer on top of the prebuilt-image base
analyzer to extract structured storefront data (store_name, hours, phone,
is_open) from field-rep photos. Uses the standard Azure async pattern:
POST :analyze -> 202 with Operation-Location header -> poll until Succeeded.
"""
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["CU_ENDPOINT"].rstrip("/")
KEY = os.environ["CU_KEY"]
API_VERSION = os.environ.get("CU_API_VERSION", "2024-12-01-preview")
ANALYZER_ID = "summitline-storefront-analyzer"
HEADERS = {"Ocp-Apim-Subscription-Key": KEY}

SCHEMA = {
    "description": "Summitline field-rep storefront analyzer",
    "baseAnalyzerId": "prebuilt-image",
    "config": {"returnDetails": True},
    "fieldSchema": {
        "fields": {
            "store_name": {
                "type": "string", "method": "generate",
                "description": "Name shown on the store sign, verbatim."
            },
            "hours": {
                "type": "string", "method": "generate",
                "description": "Posted business hours if visible; otherwise empty string."
            },
            "phone": {
                "type": "string", "method": "generate",
                "description": "Phone number if visible, digits only; otherwise empty."
            },
            "is_open": {
                "type": "boolean", "method": "generate",
                "description": "True if an OPEN sign or open-hours indication is clearly visible."
            },
        }
    },
}


def ensure_analyzer() -> None:
    """Create the analyzer if it doesn't already exist.

    GET first — 200 means the analyzer is already authored and we're done.
    Otherwise PUT the SCHEMA. A 409 Conflict on PUT also means "already
    exists" (race between workers) and is treated as success.
    """
    url = f"{ENDPOINT}/contentunderstanding/analyzers/{ANALYZER_ID}?api-version={API_VERSION}"
    get = requests.get(url, headers=HEADERS)
    if get.status_code == 200:
        return
    put = requests.put(
        url,
        headers={**HEADERS, "Content-Type": "application/json"},
        json=SCHEMA,
    )
    if put.status_code not in (200, 201, 409):
        put.raise_for_status()


def analyze(image_bytes: bytes) -> dict:
    """Analyze an image and return the extracted fields dict.

    Flow:
      1. ensure_analyzer() — PUT the analyzer once (idempotent).
      2. POST image_bytes to :analyze with Content-Type application/octet-stream.
      3. Read the Operation-Location response header.
      4. Poll that URL every 2 seconds until status == 'Succeeded'.
      5. Return poll['result']['contents'][0]['fields'].
    """
    ensure_analyzer()
    url = f"{ENDPOINT}/contentunderstanding/analyzers/{ANALYZER_ID}:analyze?api-version={API_VERSION}"
    r = requests.post(
        url,
        headers={**HEADERS, "Content-Type": "application/octet-stream"},
        data=image_bytes,
    )
    r.raise_for_status()
    op = r.headers["Operation-Location"]
    while True:
        poll = requests.get(op, headers=HEADERS).json()
        status = poll.get("status")
        if status == "Succeeded":
            return poll["result"]["contents"][0].get("fields", {})
        if status == "Failed":
            raise RuntimeError(poll)
        time.sleep(2)
