"""Drive a few example questions through the deployed /ask endpoint."""
from __future__ import annotations

import argparse
import json

import httpx

QUESTIONS = [
    ("acme", "How long do I have to file a wet-cargo claim?"),
    ("acme", "What's DHL's liability cap for ocean freight?"),
    ("contoso", "When must I submit cold-chain logger data to UPS?"),
    ("fabrikam", "What do I do if a container's seal is broken on arrival?"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    args = ap.parse_args()
    for tenant, q in QUESTIONS:
        r = httpx.post(
            f"{args.url}/ask",
            json={"tenant": tenant, "question": q},
            timeout=60,
        )
        r.raise_for_status()
        payload = r.json()
        print(f"\n=== Q ({tenant}): {q}")
        print(f"  answer: {payload['answer'][:200]}")
        print(f"  hits: {len(payload['hits'])}")


if __name__ == "__main__":
    main()
