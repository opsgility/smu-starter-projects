"""OpenTelemetry + Azure Monitor wiring for the Summitline multi-agent app.

A single call to :func:`azure.monitor.opentelemetry.configure_azure_monitor`
registers the Azure Monitor span/metric/log exporters AND auto-instruments
FastAPI, ``requests``, and the ``azure-ai-agents`` SDK, so every ``/request``
becomes one end-to-end transaction in Application Insights with:

- ``requests`` — the incoming FastAPI call (parent span).
- ``dependencies`` — agent runs (``create_and_process``), connected-agent
  sub-runs, and the individual tool-call spans from ``_refund`` / ``_lookup_order``.

Students are expected to attach a handful of custom attributes on the
``handle_request`` span created in ``app/main.py`` so they surface in
``customDimensions`` in the Logs query:

- ``summitline.customer_id`` — the caller's customer id.
- ``summitline.message_length`` — length of the incoming message.
- ``summitline.status`` — terminal status of the request ("ok" / "error").

Exercises
---------
* Exercise 3393, Step 3 — implement ``init()``.

Ordering
--------
``init()`` MUST run before ``app = FastAPI()`` is constructed in
``app/main.py``. Auto-instrumentation hooks FastAPI middleware at
construction time; configure OTel after that and the hook is missed and
incoming requests never show up as parent spans.
"""

from __future__ import annotations

import os

from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace


def init() -> "trace.Tracer":
    """Configure Azure Monitor OpenTelemetry and return the app tracer.

    Reads ``APPLICATIONINSIGHTS_CONNECTION_STRING`` from the process
    environment (populated by ``python-dotenv`` in ``main.py``). Returns the
    ``"summitline-concierge"`` tracer for the FastAPI module to use when
    wrapping ``/request`` in a custom span.

    Implementation requirements:
    - Call ``configure_azure_monitor(connection_string=...)`` exactly once.
    - Return ``trace.get_tracer("summitline-concierge")``.
    - Do NOT install a custom ``TracerProvider`` — the distro installs one.
    """
    # TODO (Exercise 3393 Step 3): call configure_azure_monitor with the
    # APPLICATIONINSIGHTS_CONNECTION_STRING env var and return
    # trace.get_tracer("summitline-concierge").
    raise NotImplementedError("Exercise 3393 Step 3: implement tracing.init()")
