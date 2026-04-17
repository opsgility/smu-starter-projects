"""
End-to-end smoke test for the capstone API. Run the server first:

    uvicorn app.main:app --reload --port 8000

Then in another terminal:

    python test_client.py
"""
from pathlib import Path

import requests

BASE = "http://127.0.0.1:8000"
HERE = Path(__file__).parent


def main() -> None:
    print("health:", requests.get(f"{BASE}/health").json())

    print("\n/chat:")
    print(requests.post(f"{BASE}/chat", data={"message": "Recommend a gift under $50."}).json())

    print("\n/analyze-text:")
    print(requests.post(
        f"{BASE}/analyze-text",
        data={"content": "Shipping was fast but the box arrived dented."},
    ).json())

    image = HERE / "sample_data" / "storefront.jpg"
    if image.exists():
        print("\n/analyze-image:")
        with image.open("rb") as f:
            print(requests.post(
                f"{BASE}/analyze-image",
                files={"file": f},
                data={"question": "What store is this?"},
            ).json())

    pdf = HERE / "sample_data" / "invoice.pdf"
    if pdf.exists():
        print("\n/extract-document:")
        with pdf.open("rb") as f:
            print(requests.post(f"{BASE}/extract-document", files={"file": f}).json())

    print("\n/speak:")
    resp = requests.post(f"{BASE}/speak", data={"content": "Welcome to Northwind Horizon."})
    (HERE / "reply.wav").write_bytes(resp.content)
    print("Saved reply.wav")


if __name__ == "__main__":
    main()
