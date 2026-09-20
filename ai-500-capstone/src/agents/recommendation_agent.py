"""Recommendation composer — L11. Calls Foundry to write a plain-English recommendation."""
from __future__ import annotations

from typing import Any

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient


def compose_recommendation(
    profile: dict[str, Any], risk_score: float, *, endpoint: str, model: str
) -> str:
    """One Foundry chat round-trip. Kept small so the capstone deploy path is fast to test."""
    client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
    chat = client.inference.get_chat_completions_client()
    response = chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are Ridgevault's portfolio adviser. Give a 2-sentence recommendation.",
            },
            {
                "role": "user",
                "content": (
                    f"Customer risk tolerance: {profile.get('risk_tolerance', 'medium')}. "
                    f"Computed portfolio risk score: {risk_score:.2f}. "
                    "Recommend one concrete rebalancing action."
                ),
            },
        ],
    )
    return response.choices[0].message.content.strip()
