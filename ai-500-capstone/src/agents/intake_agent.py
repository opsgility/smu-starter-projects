"""Intake agent — parses the customer profile blob into a structured dict.

Built in L3. This stub keeps the shape stable so the capstone smoke-tests pass; swap in the
richer L3 implementation as Exercise 2 asks.
"""
from __future__ import annotations


def parse_customer_profile(profile_text: str) -> dict[str, str | int]:
    """Return a stripped-down profile dict. Real L3 version calls the Foundry chat model."""
    return {
        "age_band": "unknown",
        "risk_tolerance": "medium",
        "raw_text_length": len(profile_text),
    }
