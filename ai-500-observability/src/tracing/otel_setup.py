"""Idempotent OpenTelemetry setup for the Ridgevault portfolio-review flow.

Configures the Azure Monitor OpenTelemetry distro against
`APPLICATIONINSIGHTS_CONNECTION_STRING`, and enables the Foundry Tracing
GenAI content-capture toggle so prompts + completions land on spans.

Call `configure_observability()` ONCE at process start, before the first
agent call. Subsequent calls are no-ops (guarded by `_configured`).
"""
from __future__ import annotations
import os

from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

_configured = False

# GenAI semantic-convention attribute keys used by App Insights + Foundry Tracing.
GEN_AI_SYSTEM = "gen_ai.system"
GEN_AI_MODEL = "gen_ai.request.model"
GEN_AI_AGENT = "gen_ai.agent.name"
GEN_AI_INPUT_TOKENS = "gen_ai.usage.input_tokens"
GEN_AI_OUTPUT_TOKENS = "gen_ai.usage.output_tokens"


def configure_observability(service_name: str = "ridgevault-portfolio-flow") -> trace.Tracer:
    """Wire OTel -> App Insights + Foundry Tracing. Returns a tracer named after this service."""
    global _configured
    if _configured:
        return trace.get_tracer(service_name)

    conn = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING", "")
    if not conn or "<" in conn:
        raise RuntimeError(
            "APPLICATIONINSIGHTS_CONNECTION_STRING is not set (angle-bracket placeholder). "
            "Copy the value from the lab Environment tab into .env, then re-run."
        )

    # Foundry Tracing consumes the same OTel spans as App Insights when this
    # env var is set — it makes chat-completions prompts + responses visible
    # in the Foundry portal Tracing tab as well as in App Insights.
    os.environ.setdefault("AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED", "true")

    configure_azure_monitor(
        connection_string=conn,
        resource_attributes={"service.name": service_name},
    )
    _configured = True
    return trace.get_tracer(service_name)
