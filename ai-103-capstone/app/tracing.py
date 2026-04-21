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
    # TODO (Exercise 1 Step 6): call configure_azure_monitor(connection_string=...)
    # using os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"].

    # TODO (Exercise 1 Step 6): return trace.get_tracer("summitline-capstone").
    raise NotImplementedError("Complete TODOs in app/tracing.py (Exercise 1 Step 6).")
