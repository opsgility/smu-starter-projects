"""Extract structured fields from a document via Content Understanding REST."""
from __future__ import annotations

import time
from pathlib import Path

import requests

from _common import ANALYZER_ID, analyze_url, bearer

SAMPLE = Path(__file__).parent.parent / "sample_data" / "invoice.md"


def extract(path: Path) -> dict:
    """TODO (exercise): POST the file, poll the operation URL, return the `result` JSON."""
    token = bearer()
    with path.open("rb") as f:
        resp = requests.post(
            analyze_url("documents"),
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/octet-stream"},
            data=f.read(),
            timeout=120,
        )
    resp.raise_for_status()
    # TODO: implement the long-running-operation poll loop. For now, just return the first response.
    _ = resp.headers.get("Operation-Location")
    time.sleep(0)
    return resp.json()


def main() -> None:
    print(f"analyzer: {ANALYZER_ID}")
    print(f"input: {SAMPLE}")
    print("result (TODO: poll operation URL):")
    print(extract(SAMPLE))


if __name__ == "__main__":
    main()
