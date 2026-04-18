"""Capstone smoke test. Start server first: uvicorn app.main:app --reload --port 8000"""
from pathlib import Path

import requests

BASE = "http://127.0.0.1:8000"
HERE = Path(__file__).parent


def main() -> None:
    print("health:", requests.get(f"{BASE}/health").json())

    print("\n/chat:")
    print(requests.post(f"{BASE}/chat", data={"message": "Recommend a gift under $50."}).json())

    print("\n/rag:")
    print(requests.post(f"{BASE}/rag", data={"question": "What is our return policy?"}).json())

    print("\n/agent:")
    print(requests.post(f"{BASE}/agent", data={"message": "What's the status of order ORD-1234?"}).json())

    image = HERE / "sample_data" / "storefront.jpg"
    if image.exists():
        print("\n/vision-ask:")
        with image.open("rb") as f:
            print(requests.post(f"{BASE}/vision-ask", files={"image": f},
                                data={"question": "What is in this image?"}).json())

    pdf = HERE / "sample_data" / "invoice.pdf"
    if pdf.exists():
        print("\n/extract-doc:")
        with pdf.open("rb") as f:
            print(requests.post(f"{BASE}/extract-doc", files={"file": f}).json())


if __name__ == "__main__":
    main()
