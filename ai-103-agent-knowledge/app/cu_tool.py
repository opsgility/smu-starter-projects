"""Azure AI Content Understanding helper used by the Summitline concierge.

This module exposes a single function, ``extract_invoice``, that the agent
registers as a ``FunctionTool`` in Exercise 3. The function:

1. Ensures a Content Understanding analyzer named ``ANALYZER_ID`` exists
   (idempotent ``PUT``).
2. Submits a PDF for analysis via ``POST ...:analyze``.
3. Polls the ``Operation-Location`` header until the LRO completes.
4. Returns the extracted fields as a JSON string.

The docstring on ``extract_invoice`` is load-bearing: ``FunctionTool`` parses
it to produce the tool schema the model sees. Do not drop ``:param file_path:``.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# --- Constants --------------------------------------------------------------
# These are read at module import time so the FunctionTool can be built
# without re-reading environment variables per invocation.

ENDPOINT: str = os.environ.get("CU_ENDPOINT", "")
API_VERSION: str = os.environ.get("CU_API_VERSION", "2024-12-01-preview")
ANALYZER_ID: str = "summitline-invoice"
HEADERS: dict[str, str] = {
    "Ocp-Apim-Subscription-Key": os.environ.get("CU_KEY", ""),
}


def extract_invoice(file_path: str) -> str:
    """Extract structured fields from an invoice PDF.

    :param file_path: Absolute path to a PDF invoice.
    :return: JSON string of extracted fields (VendorName, InvoiceTotal,
        InvoiceDate, LineItems, etc.).
    """
    # Exercise 3 - Step 1 Start
    raise NotImplementedError("Complete Exercise 3 Step 1")
    # Exercise 3 - Step 1 End
