"""Current per-model pricing for the Claude API (USD per million tokens).

Verified against https://platform.claude.com/docs/en/docs/about-claude/pricing
on 2026-09-27. If you are running this benchmark months later, cross-check
these numbers against the live pricing page before drawing conclusions —
Anthropic has changed pricing before (Sonnet 5's introductory rate became
permanent 2026-09-01, for example).

Shape: `PRICING[model_id] = (input_per_MTok, output_per_MTok)` in USD.
"""

PRICING: dict[str, tuple[float, float]] = {
    "claude-haiku-4-5":  (1.0,  5.0),
    "claude-sonnet-5":   (2.0, 10.0),
    "claude-opus-5-5":   (4.0, 20.0),
    "claude-fable-5-1": (10.0, 50.0),
}


def compute_cost_usd(model_id: str, input_tokens: int, output_tokens: int) -> float:
    """Compute the USD cost of a single request from token counts.

    Rounded to 6 decimal places since typical small requests cost fractions
    of a cent.
    """
    if model_id not in PRICING:
        raise KeyError(
            f"Unknown model id {model_id!r}. Add it to PRICING or check the "
            f"current pricing page at https://platform.claude.com/docs/en/docs/about-claude/pricing."
        )
    in_rate, out_rate = PRICING[model_id]
    cost = (input_tokens / 1_000_000) * in_rate + (output_tokens / 1_000_000) * out_rate
    return round(cost, 6)
