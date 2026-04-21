"""/extract-doc — Azure AI Content Understanding REST client (Exercise 3)."""

from __future__ import annotations

import os
import time

import requests
from opentelemetry import trace

ENDPOINT = os.environ.get("CU_ENDPOINT", "").rstrip("/")
KEY = os.environ.get("CU_KEY", "")
API_VERSION = "2024-12-01-preview"
ANALYZER_ID = "summitline-capstone-analyzer"

HEADERS = {"Ocp-Apim-Subscription-Key": KEY}

tracer = trace.get_tracer("summitline-capstone")

# TODO (Exercise 3 Step 2): define the SCHEMA dict used by _ensure() below.
# It should have baseAnalyzerId="prebuilt-documentAnalyzer" and a fieldSchema
# with three generate-method fields: vendor, doc_type, total.


def _ensure() -> None:
    """Idempotently create the Content Understanding analyzer.

    First call: GET returns 404 -> PUT the SCHEMA.
    Subsequent calls: GET returns 200 -> no-op.
    """
    # TODO (Exercise 3 Step 2): implement GET then conditional PUT using SCHEMA.
    raise NotImplementedError(
        "Complete TODOs in app/cu.py (Exercise 3 Step 2)."
    )


def extract(file_bytes: bytes) -> dict:
    """Extract ``vendor``/``doc_type``/``total`` from a document.

    POSTs the bytes to ``:analyze``, polls ``Operation-Location`` until
    ``Succeeded``, and returns the ``fields`` dict from the first content.
    """
    with tracer.start_as_current_span("summitline.cu.extract") as span:
        span.set_attribute("file.bytes", len(file_bytes))

        # TODO (Exercise 3 Step 2): call _ensure(). POST file_bytes to
        # f"{ENDPOINT}/contentunderstanding/analyzers/{ANALYZER_ID}:analyze?api-version={API_VERSION}"
        # with Content-Type: application/octet-stream. Capture Operation-Location
        # from the response headers and poll it until status == "Succeeded".
        # Return poll["result"]["contents"][0].get("fields", {}). On "Failed", raise.
        raise NotImplementedError(
            "Complete TODOs in app/cu.py (Exercise 3 Step 2)."
        )
