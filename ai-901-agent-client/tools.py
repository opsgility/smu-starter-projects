"""
Sample function-tool definitions you can attach to your Foundry agent.
Registering real tools is optional in Lesson 6 — the exercise uses the
agent's built-in knowledge by default.
"""
from typing import Any


def get_store_hours(store_id: str) -> dict[str, Any]:
    """Return operating hours for a given Northwind Horizon store id."""
    # TODO (optional): wire this to a real data source or return a hardcoded dict.
    return {
        "store_id": store_id,
        "monday_friday": "09:00-21:00",
        "saturday": "10:00-20:00",
        "sunday": "11:00-18:00",
    }


def lookup_return_policy(category: str) -> str:
    """Return the return policy text for a product category."""
    policies = {
        "electronics": "30-day return with original packaging.",
        "apparel": "60-day return with tags attached.",
        "grocery": "Non-returnable.",
    }
    return policies.get(category, "Standard 30-day return with receipt.")
