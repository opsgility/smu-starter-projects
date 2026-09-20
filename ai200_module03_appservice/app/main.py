"""Northwind Logistics shipment-classifier — Module 3 build.

Extends the Module 2 service with:

- /healthz returning explicit JSON (used by App Service health-check pings)
- /secrets-check that prints which env-var-backed secrets are wired
  (the lab uses Key Vault references for the values)
"""
from __future__ import annotations

import os
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Northwind Shipment Classifier",
    version="1.1.0",
    description="Module 3 build — adds /healthz and /secrets-check.",
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
    return {"status": "ok", "version": app.version}


@app.get("/secrets-check")
async def secrets_check() -> dict[str, dict[str, str]]:
    """Reports which env-var-backed secrets are populated.

    NEVER returns the secret values themselves — only "present" or "missing".
    The lab uses Key Vault references for these env vars; this endpoint
    is how you confirm the App Settings page wired them correctly.
    """
    keys = ["DOWNSTREAM_API_KEY", "FEATURE_FLAG_ENDPOINT", "APPINSIGHTS_CONNECTION_STRING"]
    report = {}
    for k in keys:
        value = os.environ.get(k, "")
        report[k] = {
            "present": "true" if value else "false",
            "length": str(len(value)),
        }
    return {"secrets": report}
