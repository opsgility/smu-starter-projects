"""OTel + Azure Monitor — pre-written, called on import in app/main.py."""
from __future__ import annotations

import logging
import os

from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource

_tracer = None


def tracer():
    global _tracer
    if _tracer is None:
        cs = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
        if cs:
            resource = Resource.create({"service.name": "northwind-capstone"})
            configure_azure_monitor(connection_string=cs, resource=resource)
        _tracer = trace.get_tracer("northwind-capstone")
        logging.getLogger("northwind").setLevel(logging.INFO)
    return _tracer
