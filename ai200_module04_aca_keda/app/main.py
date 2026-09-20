"""Northwind shipment-classifier — Module 4 build.

Adds an async /process endpoint that takes longer to handle so we can
exercise HTTP-scaler autoscale, plus echoes the replica name so we can
see traffic spreading across replicas after KEDA scales out.
"""
from __future__ import annotations

import asyncio
import os
import socket
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Northwind Shipment Classifier", version="1.2.0")

REPLICA = os.environ.get("HOSTNAME", socket.gethostname())


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
    return {"status": "ok", "replica": REPLICA}


@app.post("/classify", response_model=ClassifyResponse)
async def classify(req: ClassifyRequest) -> ClassifyResponse:
    label = simple_rules(req.description)
    return ClassifyResponse(shipment_id=req.shipment_id, label=label, replica=REPLICA)  # type: ignore[arg-type]


@app.post("/process")
async def process(req: ClassifyRequest) -> dict[str, str]:
    """Deliberately slow endpoint (250ms CPU + 250ms wait) so a load
    generator can drive concurrent-request counts high enough to trigger
    KEDA's HTTP scaler. Returns the replica name."""
    label = simple_rules(req.description)
    # busy CPU
    n = 0
    for _ in range(80_000):
        n = (n + 7) % 1_000_003
    # then yield
    await asyncio.sleep(0.25)
    return {"shipment_id": req.shipment_id, "label": label, "replica": REPLICA, "n": str(n)}
