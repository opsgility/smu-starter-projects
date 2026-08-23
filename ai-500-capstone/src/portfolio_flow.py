"""Ridgevault portfolio-review multi-agent flow — the production surface.

Wraps the L3-L17 building blocks (intake, risk scoring, recommendation) behind a FastAPI HTTP
service so it can run on Azure Container Apps. The /healthz endpoint is what Container Apps'
ingress probes and the CI/CD workflow smoke-tests.
"""
from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .agents.intake_agent import parse_customer_profile
from .agents.risk_agent import score_risk
from .agents.recommendation_agent import compose_recommendation


class PortfolioRequest(BaseModel):
    customer_id: str
    profile_text: str
    portfolio_holdings: list[dict[str, Any]]


class PortfolioResponse(BaseModel):
    customer_id: str
    risk_score: float
    recommendation: str
    revision: str


app = FastAPI(title="Ridgevault Portfolio Review", version="1.0.0")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    """Liveness probe — Container Apps uses this to gate traffic to a new revision."""
    return {
        "status": "ok",
        "model": os.getenv("FOUNDRY_MODEL", "unset"),
        "revision": os.getenv("CONTAINER_APP_REVISION", "local"),
    }


@app.post("/review", response_model=PortfolioResponse)
def review(request: PortfolioRequest) -> PortfolioResponse:
    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    model = os.getenv("FOUNDRY_MODEL")
    if not endpoint or not model:
        raise HTTPException(status_code=500, detail="FOUNDRY_PROJECT_ENDPOINT / FOUNDRY_MODEL not set")

    profile = parse_customer_profile(request.profile_text)
    risk = score_risk(profile, request.portfolio_holdings)
    rec = compose_recommendation(profile, risk, endpoint=endpoint, model=model)

    return PortfolioResponse(
        customer_id=request.customer_id,
        risk_score=risk,
        recommendation=rec,
        revision=os.getenv("CONTAINER_APP_REVISION", "local"),
    )
