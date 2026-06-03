"""FastAPI `/chat` endpoint for the SIB OSINT Concierge RAG pipeline.

Exercise 3, Step 1 asks you to fill in the `/chat` handler so it grounds the
Foundry Responses API on the top-k chunks from `retrieval.search`.

Run with:

    uvicorn app.main:app --reload --port 8000
"""
from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI, Form

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

from app import retrieval

load_dotenv()

# ---------------------------------------------------------------------------
# System prompt — forces the model to answer only from retrieved context
# ---------------------------------------------------------------------------

SYSTEM = (
    "You are the Sentinel Intelligence Bureau OSINT Concierge support "
    "assistant. Answer the analyst's question using ONLY the passages "
    "provided in the Context section. If the context does not contain the "
    "answer, say you don't know and suggest they consult the SIB OSINT "
    "Modernization team. "
    "Always cite sources by filename in square brackets, for example "
    "[collection-policy.md]."
)

# ---------------------------------------------------------------------------
# Shared clients built once at import time
# ---------------------------------------------------------------------------

_project_endpoint = os.environ.get("AZURE_AI_PROJECT_ENDPOINT", "")
_deployment = os.environ.get("MODEL_DEPLOYMENT", "gpt-4.1-mini")

_project = AIProjectClient(
    endpoint=_project_endpoint,
    credential=DefaultAzureCredential(),
)

app = FastAPI(title="Sentinel Intelligence Bureau OSINT Concierge - RAG")


@app.get("/health")
def health() -> dict:
    """Liveness probe."""
    return {"status": "ok"}


@app.post("/chat")
def chat(message: str = Form(...)) -> dict:
    """Answer `message` using retrieved SIB OSINT context.

    Expected response shape:

        {
          "reply":   "<model response with [source.md] citations>",
          "sources": ["collection-policy.md", "osint-handbook.md", ...]
        }
    """
    # Exercise 3 - Step 1 Start
    raise NotImplementedError("Complete Exercise 3 Step 1")
    # Exercise 3 - Step 1 End
