"""Northwind shipment-classifier — Module 5 (AKS) build.

Same surface as Module 4 plus a /readyz endpoint distinct from /healthz —
AKS uses readinessProbe and livenessProbe separately and they should not
share the same endpoint.
"""
from __future__ import annotations

import asyncio
import os
import socket
import time
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Northwind Shipment Classifier", version="1.3.0")
REPLICA = os.environ.get("HOSTNAME", socket.gethostname())
STARTED_AT = time.time()


class ClassifyRequest(BaseModel):
    shipment_id: str = Field(..., examples=["ship-001"])
    description: str = Field(..., examples=["package soaked from rain"])


class ClassifyResponse(BaseModel):
    shipment_id: str
    label: Literal[
        "water-damage", "crush-damage", "missing-item",
        "delayed", "temperature-excursion", "unknown",
    ]
    replica: str


RULES = [
    (("water", "soaked", "wet", "rain", "flood"), "water-damage"),
    (("crushed", "crush", "smashed", "broken", "dent"), "crush-damage"),
    (("missing", "lost", "stolen", "not found"), "missing-item"),
    (("late", "delayed", "delay", "stuck"), "delayed"),
    (("frozen", "thawed", "warm", "spoiled", "temperature"), "temperature-excursion"),
]


def simple_rules(description: str) -> str:
    text = description.lower()
    for keywords, label in RULES:
        if any(k in text for k in keywords):
            return label
    return "unknown"


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    """Liveness — does the process respond at all?"""
    return {"status": "ok", "replica": REPLICA}


@app.get("/readyz")
async def readyz() -> dict[str, str]:
    """Readiness — only ready 5s after startup, simulating warm-up."""
    uptime = time.time() - STARTED_AT
    if uptime < 5:
        return {"status": "starting", "uptime_s": f"{uptime:.1f}"}
    return {"status": "ready", "uptime_s": f"{uptime:.1f}"}


@app.post("/classify", response_model=ClassifyResponse)
async def classify(req: ClassifyRequest) -> ClassifyResponse:
    label = simple_rules(req.description)
    return ClassifyResponse(shipment_id=req.shipment_id, label=label, replica=REPLICA)  # type: ignore[arg-type]


@app.post("/process")
async def process(req: ClassifyRequest) -> dict[str, str]:
    label = simple_rules(req.description)
    n = 0
    for _ in range(80_000):
        n = (n + 7) % 1_000_003
    await asyncio.sleep(0.25)
    return {"shipment_id": req.shipment_id, "label": label, "replica": REPLICA, "n": str(n)}
