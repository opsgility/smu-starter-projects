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

# Exercise 3 - Step 2 Start
SCHEMA: dict = {}
# Exercise 3 - Step 2 End


def _ensure() -> None:
    """Idempotently create the Content Understanding analyzer.

    First call: GET returns 404 -> PUT the SCHEMA.
    Subsequent calls: GET returns 200 -> no-op.
    """
    # Exercise 3 - Step 2 Start
    raise NotImplementedError("Complete Exercise 3 Step 2")
    # Exercise 3 - Step 2 End


def extract(file_bytes: bytes) -> dict:
    """Extract ``vendor``/``doc_type``/``total`` from a document.

    POSTs the bytes to ``:analyze``, polls ``Operation-Location`` until
    ``Succeeded``, and returns the ``fields`` dict from the first content.
    """
    with tracer.start_as_current_span("summitline.cu.extract") as span:
        span.set_attribute("file.bytes", len(file_bytes))

        # Exercise 3 - Step 2 Start
        raise NotImplementedError("Complete Exercise 3 Step 2")
        # Exercise 3 - Step 2 End
