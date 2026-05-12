"""Drive enough traffic at the deployed app to produce a usable trace dataset."""
from __future__ import annotations

import argparse
import random
import time

import httpx

DESCRIPTIONS = [
    "package soaked from rain",
    "crate crushed in transit",
    "item missing from shipment",
    "shipment delayed at port",
    "outer box dented",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--count", type=int, default=200)
    args = ap.parse_args()
    for i in range(args.count):
        body = {"shipment_id": f"otel-{i:04d}", "description": random.choice(DESCRIPTIONS)}
        try:
            httpx.post(f"{args.url}/classify", json=body, timeout=10)
        except Exception as exc:  # noqa: BLE001
            print(f"err {i}: {exc}")
        if (i + 1) % 25 == 0:
            print(f"sent {i+1}")
        time.sleep(0.05)


if __name__ == "__main__":
    main()
