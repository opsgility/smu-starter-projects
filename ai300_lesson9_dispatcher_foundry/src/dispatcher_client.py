"""Local smoke-test client for the Dispatcher API.

Runs a handful of scripted messages against a locally-running
``dispatcher_api`` and prints the routing verdict for each. Useful as a
sanity check before opening a PR that triggers ``promote-prompt.yml``.

Usage:
    uvicorn src.dispatcher_api:app --reload --port 8000
    # in another terminal:
    python src/dispatcher_client.py
"""

from __future__ import annotations

import os
import sys

import httpx

BASE_URL = os.environ.get("DISPATCHER_URL", "http://127.0.0.1:8000")

MESSAGES: list[tuple[str, str]] = [
    ("battery-dead", "My car battery is dead and I'm stuck in the Target parking lot."),
    ("bill-shock", "Why did my premium jump $60 this month? I'm on autopay."),
    ("new-claim", "I need to file a claim — someone rear-ended me at the light."),
    ("add-driver", "Please add my daughter Ava to my policy — she just got her license."),
    ("lawyer", "I'm getting my lawyer involved. This is the third time you've botched this."),
]


def main() -> int:
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        health = client.get("/healthz")
        health.raise_for_status()
        print(f"healthz: {health.json()}\n")

        rc = 0
        for label, msg in MESSAGES:
            resp = client.post("/dispatch", json={"message": msg})
            if resp.status_code != 200:
                print(f"[{label}] FAIL status={resp.status_code} body={resp.text}")
                rc = 1
                continue
            j = resp.json()
            print(
                f"[{label}] queue={j['queue']:<15} "
                f"conf={j['confidence']:.2f} "
                f"reason={j['reason']!r} "
                f"prompt={j['prompt_version']}"
            )
        return rc


if __name__ == "__main__":
    sys.exit(main())
