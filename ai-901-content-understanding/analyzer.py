"""
Shared helpers for Azure Content Understanding.

The Content Understanding service is REST-based (preview at exam publication time).
You'll implement:
  - create_or_update_analyzer(schema_json)
  - submit_content(analyzer_id, file_bytes, content_type)
  - poll_result(operation_url)

All three are used by the per-asset-type scripts.
"""
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

HEADERS = {"Ocp-Apim-Subscription-Key": KEY}


def create_or_update_analyzer(analyzer_id: str, schema: dict) -> None:
    """PUT /contentunderstanding/analyzers/{analyzerId}?api-version=..."""
    # TODO 1: PUT to f"{ENDPOINT}/contentunderstanding/analyzers/{analyzer_id}?api-version={API_VERSION}"
    #         with HEADERS + json=schema. Raise for status.
    raise NotImplementedError


def submit_content(analyzer_id: str, file_path: Path, content_type: str) -> str:
    """POST the file bytes to the analyze endpoint; return the operation URL."""
    # TODO 2: POST to f"{ENDPOINT}/contentunderstanding/analyzers/{analyzer_id}:analyze?api-version={API_VERSION}"
    #         headers include Content-Type=content_type + HEADERS; body=file bytes.
    #         Return response.headers["Operation-Location"].
    raise NotImplementedError


def poll_result(operation_url: str, timeout_sec: int = 120) -> dict:
    """Poll the operation URL until the status is 'Succeeded' or 'Failed'."""
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        # TODO 3: GET operation_url with HEADERS. If status == "Succeeded" return the response JSON.
        #         If status == "Failed" raise RuntimeError. Otherwise sleep 2 and continue.
        raise NotImplementedError
    raise TimeoutError("Content Understanding analyze operation did not complete in time.")


def load_schema(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))
