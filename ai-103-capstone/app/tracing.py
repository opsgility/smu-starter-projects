"""OTel + Azure Monitor."""
import os

from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace


def init() -> trace.Tracer:
    # TODO 1: configure_azure_monitor(connection_string=
    #         os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]).
    # TODO 2: return trace.get_tracer("ai-103-capstone").
    raise NotImplementedError
