"""AI-3016 Lesson 9 — call Aurora's deployed prompt flow from Python.

The flow endpoint is what your production app POSTs to. It runs the whole
DAG (sanitize -> classify_intent -> retrieve -> answer) and returns the
final response with citations.

This is different from lesson 6, which called the RAW model deployment.
The flow endpoint sits in front of the model deployments and orchestrates.
"""

import os
import json
import requests
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential


def call_flow(user_question: str, chat_history: list[dict] | None = None) -> dict:
    """POST to the deployed flow endpoint and return the flow's outputs."""
    endpoint = os.environ["AURORA_FLOW_ENDPOINT"]

    # Managed Identity token for the Azure ML workspace scope.
    credential = DefaultAzureCredential()
    token = credential.get_token("https://ml.azure.com/.default").token

    body = {
        "chat_history": chat_history or [],
        "user_question": user_question,
    }

    response = requests.post(
        endpoint,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        data=json.dumps(body),
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def demo() -> None:
    questions = [
        "hi",
        "What is Aurora's engagement methodology?",
        "What was Acme Corp's Athena project delivery date?",
    ]
    for q in questions:
        print(f"\n=== USER: {q} ===")
        result = call_flow(q)
        print(f"ANSWER: {result.get('answer', '(no answer key)')}\n")
        sources = result.get("sources", [])
        if sources:
            print("SOURCES:")
            for i, s in enumerate(sources, 1):
                print(f"  [{i}] {s.get('filepath', s.get('source', '?'))}")


if __name__ == "__main__":
    load_dotenv()
    demo()
