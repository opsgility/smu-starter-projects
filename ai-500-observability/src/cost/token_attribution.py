"""Per-agent-turn token attribution.

Extracts prompt + completion + total token counts from a Foundry chat-completions
response and tags them on the current OTel span using the GenAI semantic
convention that App Insights + Foundry Tracing both recognize.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from opentelemetry import trace

# gpt-5 chat pricing per 1K tokens (approximate — verify against the current
# Foundry pricing sheet before invoicing anyone). Kept here as constants so the
# token_attribution.attribute_tokens_on_span function can multiply them out for
# a rough per-turn cost estimate. Model routing labs override MODEL_COSTS.
MODEL_COSTS: dict[str, tuple[float, float]] = {
    "gpt-5": (1.25 / 1000, 10.00 / 1000),
    "gpt-5-mini": (0.25 / 1000, 2.00 / 1000),
}


@dataclass
class TurnCost:
    agent: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    est_usd: float


def attribute_tokens_on_span(*, agent: str, model: str, response: Any) -> TurnCost:
    """Read usage off a chat.completions response and stamp it on the active span.

    Returns a TurnCost the caller can accumulate for a per-agent bar chart.
    """
    usage = getattr(response, "usage", None)
    prompt = int(getattr(usage, "prompt_tokens", 0) or 0)
    completion = int(getattr(usage, "completion_tokens", 0) or 0)
    total = int(getattr(usage, "total_tokens", prompt + completion) or (prompt + completion))

    p_rate, c_rate = MODEL_COSTS.get(model, (0.0, 0.0))
    est = round(prompt * p_rate + completion * c_rate, 6)

    span = trace.get_current_span()
    span.set_attribute("gen_ai.agent.name", agent)
    span.set_attribute("gen_ai.request.model", model)
    span.set_attribute("gen_ai.usage.input_tokens", prompt)
    span.set_attribute("gen_ai.usage.output_tokens", completion)
    span.set_attribute("gen_ai.usage.total_tokens", total)
    span.set_attribute("ridgevault.est_usd", est)

    return TurnCost(
        agent=agent, model=model,
        prompt_tokens=prompt, completion_tokens=completion,
        total_tokens=total, est_usd=est,
    )
