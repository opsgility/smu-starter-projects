"""OpenTelemetry + Azure Monitor wiring.

Student fills in the TODOs in Step 4.
"""
from __future__ import annotations

import logging
import os

from opentelemetry import trace
from opentelemetry.trace import Tracer

_TRACER: Tracer | None = None


def configure(service_name: str = "northwind-classifier") -> Tracer:
    """Configure Azure Monitor + OTel and return a tracer.

    TODO(step4): replace this body. The function must:
      1. Read APPLICATIONINSIGHTS_CONNECTION_STRING from os.environ
      2. Call configure_azure_monitor(connection_string=..., logger_name="northwind")
         from azure.monitor.opentelemetry
      3. Set OTEL_SERVICE_NAME on the resource (set env var before configure_azure_monitor,
         or pass resource_attributes)
      4. tracer = trace.get_tracer(service_name)
      5. Store in module global _TRACER and return it.

    Hint: passing resource_attributes is the cleanest way:
        from opentelemetry.sdk.resources import Resource
        resource = Resource.create({"service.name": service_name})
        configure_azure_monitor(connection_string=cs, resource=resource)
    """
    raise NotImplementedError("Step 4: implement configure")


def tracer() -> Tracer:
    global _TRACER
    if _TRACER is None:
        _TRACER = configure()
    return _TRACER
