"""Northwind Logistics shipment-classifier FastAPI service.

A tiny rule-based classifier you can build into a container and push to ACR.
Lab module 2 - the application is already complete; the lab focuses on
build + tag + push + digest workflow with `az acr build`.
"""
from __future__ import annotations

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Northwind Shipment Classifier",
    version="1.0.0",
    description="Classifies shipment-incident descriptions into damage categories.",
)


class ClassifyRequest(BaseModel):
    shipment_id: str = Field(..., examples=["ship-001"])
    description: str = Field(..., examples=["package soaked from rain on the dock"])


class ClassifyResponse(BaseModel):
    shipment_id: str
    label: Literal[
        "water-damage",
        "crush-damage",
        "missing-item",
        "delayed",
        "temperature-excursion",
        "unknown",
    ]


# Deterministic rule-based labeller. Replaced by a real model in later modules.
RULES: list[tuple[tuple[str, ...], str]] = [
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


@app.get("/")
async def root() -> dict[str, str]:
    return {"service": "shipment-classifier", "version": app.version}


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/classify", response_model=ClassifyResponse)
async def classify(req: ClassifyRequest) -> ClassifyResponse:
    label = simple_rules(req.description)
    return ClassifyResponse(shipment_id=req.shipment_id, label=label)  # type: ignore[arg-type]
