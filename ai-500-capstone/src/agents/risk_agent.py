"""Risk-scoring agent — L7. Returns a 0.0-1.0 score for the given portfolio."""
from __future__ import annotations

from typing import Any


def score_risk(profile: dict[str, Any], holdings: list[dict[str, Any]]) -> float:
    """Naive concentration heuristic. Swap in the L7 gpt-5-scored implementation later."""
    if not holdings:
        return 0.0
    weights = [float(h.get("weight_pct", 0)) for h in holdings]
    largest = max(weights) if weights else 0.0
    concentration_penalty = min(largest / 100.0, 1.0)
    tolerance_bump = 0.1 if profile.get("risk_tolerance") == "aggressive" else 0.0
    return round(min(concentration_penalty + tolerance_bump, 1.0), 3)
