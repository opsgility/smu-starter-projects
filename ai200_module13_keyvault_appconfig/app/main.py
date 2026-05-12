"""FastAPI app that demos the secrets + config flow."""
from __future__ import annotations

from fastapi import FastAPI

from lib.config import feature_enabled, setting
from lib.secrets import get_secret

app = FastAPI(title="Northwind Config Demo", version="1.0.0")


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/config")
async def show_config() -> dict[str, object]:
    return {
        "carrier_default": setting("northwind:carrier_default"),
        "claim_window_hours": setting("northwind:claim_window_hours"),
        "fastpath_enabled": feature_enabled("fastpath"),
    }


@app.get("/secret-length")
async def secret_length() -> dict[str, int]:
    # Length only — never return the secret value.
    s = get_secret("downstream-api-key")
    return {"length": len(s or "")}
