"""Sentinel Intelligence Bureau capstone FastAPI app.

Fully wired — the exercises edit the modules imported below, not this file.
Tracing is configured at import time (before ``app = FastAPI()``) so every
route is auto-instrumented.
"""

from __future__ import annotations

# Load .env early so the SDKs see credentials at import time.
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv is in requirements.txt; safe guard anyway.
    pass

# IMPORTANT: configure Azure Monitor OTel BEFORE FastAPI is instantiated.
from app import tracing  # noqa: E402

try:
    tracing.init()
except Exception:  # pragma: no cover - students see the real error in their terminal.
    # Surfaces a clear error the first time a student runs the app without
    # finishing Exercise 1 Step 6.
    raise

from fastapi import FastAPI, Form  # noqa: E402
from fastapi.responses import JSONResponse  # noqa: E402

from app import agent, chat, rag  # noqa: E402

app = FastAPI(
    title="Sentinel Intelligence Bureau Capstone",
    description=(
        "AI-3016 capstone. Four endpoints on one Foundry project, "
        "observable end-to-end in Application Insights."
    ),
    version="1.0.0",
)


@app.get("/health")
def health() -> dict:
    """Liveness probe. Used by test_client.py first."""
    return {"status": "ok"}


@app.post("/chat")
def chat_endpoint(message: str = Form(...)) -> dict:
    """Stateless analyst chat."""
    return {"reply": chat.reply(message)}


@app.post("/rag")
def rag_endpoint(question: str = Form(...)) -> dict:
    """Grounded answer with citations from sib-osint-kb."""
    return rag.answer(question)


@app.post("/agent")
def agent_endpoint(message: str = Form(...)) -> dict:
    """Tool-using concierge (AzureAISearchTool + _indicator_status)."""
    return {"reply": agent.run(message)}


@app.exception_handler(NotImplementedError)
def _not_implemented_handler(_request, exc: NotImplementedError) -> JSONResponse:
    """Friendlier 501 when a student hits an endpoint before finishing TODOs."""
    return JSONResponse(status_code=501, content={"error": str(exc)})
