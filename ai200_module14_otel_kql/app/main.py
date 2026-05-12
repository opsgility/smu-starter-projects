"""Instrumented FastAPI app for Module 14."""
from __future__ import annotations

import logging
import random
import time

from fastapi import FastAPI
from pydantic import BaseModel

from lib.telemetry import tracer

# Initialize telemetry on import.
_t = tracer()

app = FastAPI(title="Northwind Telemetry Demo", version="1.0.0")
log = logging.getLogger("northwind")
log.setLevel(logging.INFO)


class ClassifyRequest(BaseModel):
    shipment_id: str
    description: str


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/classify")
async def classify(req: ClassifyRequest) -> dict[str, str]:
    """Demonstrates manual spans + custom attributes — the student adds
    one more span in Step 6.
    """
    with _t.start_as_current_span("classify") as span:
        span.set_attribute("shipment.id", req.shipment_id)
        span.set_attribute("tenant", "acme")

        # Simulate two downstream calls — one cheap, one variable.
        with _t.start_as_current_span("rules_lookup"):
            time.sleep(0.005 + random.random() * 0.005)

        # TODO(step6): wrap this block in a span named "vector_search"
        # and set attribute "top_k" = 5 on it. Remove these two comment lines.
        time.sleep(0.02 + random.random() * 0.06)

        label = _label(req.description)
        span.set_attribute("classifier.label", label)
        log.info("classified shipment_id=%s label=%s", req.shipment_id, label)
        return {"shipment_id": req.shipment_id, "label": label}


def _label(text: str) -> str:
    t = text.lower()
    if "water" in t or "soak" in t or "rain" in t:
        return "water-damage"
    if "crush" in t or "dent" in t:
        return "crush-damage"
    if "missing" in t or "lost" in t:
        return "missing-item"
    if "delay" in t or "stuck" in t:
        return "delayed"
    return "unknown"
