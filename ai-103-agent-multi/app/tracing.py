"""OpenTelemetry + Azure Monitor for the multi-agent app."""
import os

from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace


def init() -> trace.Tracer:
    # TODO 1: Call configure_azure_monitor(connection_string=
    #         os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]).
    # TODO 2: Return trace.get_tracer("ai-103-agent-multi").
    raise NotImplementedError
