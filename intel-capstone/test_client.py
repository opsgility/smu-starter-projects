"""Smoke test every SIB capstone endpoint (Exercise 3).

Assumes the app is running on http://127.0.0.1:8000. Run:

    python test_client.py
"""

from __future__ import annotations

import requests

BASE = "http://127.0.0.1:8000"


def _pretty(label: str, response: requests.Response) -> None:
    print(f"\n{label}:")
    try:
        print(response.json())
    except Exception:
        print(f"  status={response.status_code}  bytes={len(response.content)}")


def main() -> int:
    # 1. Health
    r = requests.get(f"{BASE}/health", timeout=10)
    print("health:", r.json())

    # 2. /chat
    r = requests.post(
        f"{BASE}/chat",
        data={"message": "Summarize the Concierge's role in two sentences."},
        timeout=60,
    )
    _pretty("/chat", r)

    # 3. /rag
    r = requests.post(
        f"{BASE}/rag",
        data={"question": "What sources are in scope for the OSINT Concierge?"},
        timeout=60,
    )
    _pretty("/rag", r)

    # 4. /agent — indicator lookup (exercises the function tool)
    r = requests.post(
        f"{BASE}/agent",
        data={"message": "What is the current status of indicator OSINT-IND-2024-1042?"},
        timeout=120,
    )
    _pretty("/agent (indicator)", r)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
