"""Ridgevault portfolio-review sequential flow, instrumented.

Three specialist agents run in sequence:

    Portfolio Analyst  -->  Risk Assessor  -->  Compliance Officer

Each turn is wrapped in an OpenTelemetry span; token usage is attributed
per agent on the span. The risk_assessor turn passes through an LRU
response cache (compression is applied to its system prompt at build time),
and the compliance_officer's output length is recorded on the drift alarm.

Run:
    python src/portfolio_flow.py

Watch:
    - App Insights > Application Map + End-to-end transaction search
    - Foundry portal > project > Tracing tab
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from opentelemetry import trace

from tracing.otel_setup import configure_observability
from cost.token_attribution import attribute_tokens_on_span, TurnCost
from optimizations.prompt_compress import compress_prompt
from optimizations.response_cache import risk_assessor_cache
from drift.output_length_alarm import compliance_length_alarm

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "test-portfolios.jsonl"

PORTFOLIO_ANALYST_SYSTEM = (
    "You are Ridgevault Financial's portfolio analyst. Given a client's positions, "
    "summarize the current allocation across equity, fixed income, and cash in 2-3 sentences. "
    "Numbers first. No advice, no opinions."
)

# Deliberately verbose so the compression pass has something to trim.
RISK_ASSESSOR_SYSTEM_RAW = (
    "As an AI risk assessment analyst for Ridgevault Financial, it is important to note that "
    "you must always identify concentration risk, sector risk, and drawdown risk in the client's "
    "portfolio. Please ensure that you always call out any single position above 15% of the "
    "portfolio, and kindly, at your earliest convenience, at this point in time flag any "
    "sector exposure above 40%. In order to keep your response short, use bullet points."
)

COMPLIANCE_OFFICER_SYSTEM = (
    "You are Ridgevault Financial's compliance officer. Review the analyst's summary and the "
    "risk flags below. State in 3-6 sentences whether the position is suitable for a "
    "moderate-risk retail client under Reg BI, referencing any specific concerns."
)


def _load_portfolios() -> list[dict]:
    with DATA_PATH.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _chat(client, model: str, system: str, user: str) -> tuple[str, object]:
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_completion_tokens=400,
    )
    text = (resp.choices[0].message.content or "").strip()
    return text, resp


def run_flow(client_id: str, positions: list[dict]) -> dict:
    """Run all three agents against one portfolio; return per-agent outputs + costs."""
    load_dotenv()
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model = os.environ["FOUNDRY_MODEL"]

    tracer = configure_observability("ridgevault-portfolio-flow")

    project = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
    openai_client = project.get_openai_client(api_version="2025-04-01-preview")

    positions_str = json.dumps(positions)
    costs: list[TurnCost] = []
    outputs: dict[str, str] = {}

    with tracer.start_as_current_span("portfolio_review_flow") as flow_span:
        flow_span.set_attribute("ridgevault.client_id", client_id)

        # 1) Portfolio Analyst.
        with tracer.start_as_current_span("agent.portfolio_analyst"):
            text, resp = _chat(openai_client, model, PORTFOLIO_ANALYST_SYSTEM, positions_str)
            costs.append(attribute_tokens_on_span(agent="portfolio_analyst", model=model, response=resp))
            outputs["portfolio_analyst"] = text

        # 2) Risk Assessor — compressed system prompt + LRU cache in front.
        with tracer.start_as_current_span("agent.risk_assessor") as span:
            risk_prompt = f"Portfolio summary:\n{outputs['portfolio_analyst']}\n\nPositions:\n{positions_str}"
            cached = risk_assessor_cache.get("risk_assessor", risk_prompt)
            if cached is not None:
                span.set_attribute("ridgevault.cache", "hit")
                outputs["risk_assessor"] = cached
            else:
                span.set_attribute("ridgevault.cache", "miss")
                compressed = compress_prompt(RISK_ASSESSOR_SYSTEM_RAW).compressed
                span.set_attribute("ridgevault.prompt_compressed_chars", len(compressed))
                text, resp = _chat(openai_client, model, compressed, risk_prompt)
                costs.append(attribute_tokens_on_span(agent="risk_assessor", model=model, response=resp))
                outputs["risk_assessor"] = text
                risk_assessor_cache.put("risk_assessor", risk_prompt, text)

        # 3) Compliance Officer + drift alarm.
        with tracer.start_as_current_span("agent.compliance_officer") as span:
            comp_prompt = (
                f"Analyst summary:\n{outputs['portfolio_analyst']}\n\n"
                f"Risk flags:\n{outputs['risk_assessor']}"
            )
            text, resp = _chat(openai_client, model, COMPLIANCE_OFFICER_SYSTEM, comp_prompt)
            costs.append(attribute_tokens_on_span(agent="compliance_officer", model=model, response=resp))
            compliance_length_alarm.record(text)
            if compliance_length_alarm.is_drifting():
                span.set_attribute("ridgevault.drift", "compliance_output_length")
            outputs["compliance_officer"] = text

    return {
        "client_id": client_id,
        "outputs": outputs,
        "costs": [c.__dict__ for c in costs],
        "cache_hit_rate_pct": risk_assessor_cache.hit_rate,
        "drift_snapshot": compliance_length_alarm.snapshot(),
    }


def main() -> int:
    portfolios = _load_portfolios()
    if not portfolios:
        print("ERROR: no portfolios in data/test-portfolios.jsonl", file=sys.stderr)
        return 1

    # Run the first portfolio end-to-end; students loop or parallelize in the exercises.
    p = portfolios[0]
    result = run_flow(p["client_id"], p["positions"])
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
