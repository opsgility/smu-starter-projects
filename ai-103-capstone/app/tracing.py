"""Azure Monitor OpenTelemetry bootstrap — Exercise 1.

This module runs at import time. ``main.py`` imports it BEFORE
``FastAPI()`` is instantiated so that every route is auto-instrumented.
"""

from __future__ import annotations

import os

from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace


def init() -> "trace.Tracer":
    """Configure Azure Monitor and return a tracer for manual spans.

    Reads ``APPLICATIONINSIGHTS_CONNECTION_STRING`` from the environment
    (populated by Exercise 1 Step 3 from the ARM deployment outputs).

    Returns
    -------
    opentelemetry.trace.Tracer
        A tracer named ``summitline-capstone`` that endpoint modules use
        to wrap custom logic spans (e.g. ``summitline.rag.search``).
    """
    # Exercise 1 - Step 6 Start
    raise NotImplementedError("Complete Exercise 1 Step 6")
    # Exercise 1 - Step 6 End
