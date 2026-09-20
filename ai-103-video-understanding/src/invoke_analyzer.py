"""Author + invoke the Summitline pro-mode video analyzer.

Implemented across Exercises 3 and 4:

  - Exercise 3 - author the pro-mode schema (already scaffolded in
    `src/analyzer_schema.json`; students refine `fieldSchema.fields`).
  - Exercise 4 TODOs 1-4 - PUT the analyzer to CU, POST :analyze against
    each uploaded video, poll operation-location, save the JSON result.

The CU service lives at `<AZURE_CU_ENDPOINT>/contentunderstanding/*`. We POST
the analyze request and then GET the URL returned in the `operation-location`
response header until `status` is `Succeeded` or `Failed`.

Run with:
    python src/invoke_analyzer.py
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import time
from typing import Any, Dict

import requests
from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential

from src.upload_videos import build_service_client, mint_user_delegation_sas, SAMPLE_URLS


load_dotenv()

CU_ENDPOINT = os.environ["AZURE_CU_ENDPOINT"].rstrip("/")
ANALYZER_ID = "summitline-video"
API_VERSION = "2025-11-01"  # GA - do NOT swap to a preview API version.
SCHEMA_PATH = pathlib.Path(__file__).parent / "analyzer_schema.json"
RESULTS_DIR = pathlib.Path(__file__).parent.parent / "data"


def _cu_headers() -> Dict[str, str]:
    """Bearer token scoped for Cognitive Services (Content Understanding accepts this)."""
    token = DefaultAzureCredential().get_token(
        "https://cognitiveservices.azure.com/.default"
    ).token
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def create_or_update_analyzer() -> Dict[str, Any]:
    """PUT the pro-mode analyzer schema to Content Understanding."""
    # Exercise 4 - TODO 1
    raise NotImplementedError(
        "Exercise 4 TODO 1: load SCHEMA_PATH as JSON, then PUT to "
        f"'{CU_ENDPOINT}/contentunderstanding/analyzers/{ANALYZER_ID}?api-version={API_VERSION}'. "
        "Call raise_for_status() and return response.json()."
    )


def analyze_video(video_sas_url: str) -> Dict[str, Any]:
    """POST :analyze with the video URL, then poll operation-location until done."""
    # Exercise 4 - TODO 2 (submit the analyze request)
    # Exercise 4 - TODO 3 (poll operation-location every 3 seconds)
    # Exercise 4 - TODO 4 (return the terminal analyze result JSON)
    raise NotImplementedError(
        "Exercise 4 TODOs 2/3/4: POST to "
        f"'{CU_ENDPOINT}/contentunderstanding/analyzers/{ANALYZER_ID}:analyze?api-version={API_VERSION}' "
        "with json={'url': video_sas_url}. Read op_url = r.headers['operation-location']. "
        "Poll GET(op_url, headers=_cu_headers()) every 3s until status is 'Succeeded' or 'Failed'. "
        "Return the final poll payload."
    )


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    analyzer = create_or_update_analyzer()
    print(f"[analyzer] created/updated: {analyzer.get('analyzerId', ANALYZER_ID)}")

    # Analyze every uploaded sample video
    service = build_service_client()
    for blob_name, _ in SAMPLE_URLS:
        sas = mint_user_delegation_sas(service, blob_name, minutes=30)
        print(f"[analyze]  {blob_name} - submitting...")
        result = analyze_video(sas)
        status = result.get("status", "?")
        segments = result.get("result", {}).get("contents", [])
        print(f"[analyze]  {blob_name} -> {status} ({len(segments)} segment(s))")

        out = RESULTS_DIR / f"analyzer_result_{blob_name.split('.')[0]}.json"
        out.write_text(json.dumps(result, indent=2))
        print(f"[saved]    {out}")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as exc:
        print(f"\n[TODO]     {exc}", file=sys.stderr)
        sys.exit(2)
