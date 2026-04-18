"""Smoke test. Start the server first: uvicorn app.main:app --reload --port 8000"""
import requests

BASE = "http://127.0.0.1:8000"

print("\n/chat (tool call expected):")
print(requests.post(f"{BASE}/chat", data={"message": "Weather in Seattle?"}).json())

print("\n/chat (no tool expected):")
print(requests.post(f"{BASE}/chat", data={"message": "Hi, what can you do?"}).json())

print("\n/stream:")
with requests.post(f"{BASE}/stream", data={"message": "Explain RAG briefly."}, stream=True) as resp:
    for chunk in resp.iter_content(chunk_size=None):
        if chunk:
            print(chunk.decode("utf-8"), end="")
print()
