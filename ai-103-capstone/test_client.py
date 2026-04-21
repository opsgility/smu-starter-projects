"""Smoke test every Summitline capstone endpoint (Exercise 4).

Assumes the app is running on http://127.0.0.1:8000. Run:

    python test_client.py
"""

from __future__ import annotations

from pathlib import Path

import requests

BASE = "http://127.0.0.1:8000"
HERE = Path(__file__).parent


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
        data={"message": "Recommend a daypack under 150 dollars for day hikes."},
        timeout=60,
    )
    _pretty("/chat", r)

    # 3. /rag
    r = requests.post(
        f"{BASE}/rag",
        data={"question": "What is Summitline's return policy?"},
        timeout=60,
    )
    _pretty("/rag", r)

    # 4. /agent — order status (exercises the function tool)
    r = requests.post(
        f"{BASE}/agent",
        data={"message": "What's the status of order SUM-884210?"},
        timeout=120,
    )
    _pretty("/agent (order)", r)

    # 5. /vision-ask — needs a JPEG on disk
    image = HERE / "sample_data" / "storefront.jpg"
    if image.exists():
        with image.open("rb") as f:
            r = requests.post(
                f"{BASE}/vision-ask",
                files={"image": ("storefront.jpg", f, "image/jpeg")},
                data={"question": "What is in this image?"},
                timeout=60,
            )
        _pretty("/vision-ask", r)
    else:
        print("\n/vision-ask: skipped (sample_data/storefront.jpg not present)")

    # 6. /extract-doc — needs a PDF on disk
    invoice = HERE / "sample_data" / "invoice.pdf"
    if invoice.exists():
        with invoice.open("rb") as f:
            r = requests.post(
                f"{BASE}/extract-doc",
                files={"file": ("invoice.pdf", f, "application/pdf")},
                timeout=120,
            )
        _pretty("/extract-doc", r)
    else:
        print("\n/extract-doc: skipped (sample_data/invoice.pdf not present)")

    # 7. /voice — optional; only runs if the student pre-generated question.wav
    audio = HERE / "question.wav"
    if audio.exists():
        with audio.open("rb") as f:
            r = requests.post(
                f"{BASE}/voice",
                files={"audio": ("question.wav", f, "audio/wav")},
                timeout=120,
            )
        reply_path = HERE / "reply.wav"
        reply_path.write_bytes(r.content)
        print(f"\n/voice: wrote {reply_path} ({len(r.content)} bytes)")
    else:
        print("\n/voice: skipped (question.wav not present; see Exercise 3 Step 4)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
