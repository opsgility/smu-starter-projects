"""FastAPI `/chat` endpoint for the Summitline Outfitters RAG concierge.

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
    "You are the Summitline Outfitters support concierge. "
    "Answer the customer's question using ONLY the passages provided in the "
    "Context section. If the context does not contain the answer, say you "
    "don't know and suggest they contact Summitline support. "
    "Always cite sources by filename in square brackets, for example "
    "[returns-policy.md]."
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

app = FastAPI(title="Summitline Outfitters RAG Concierge")


@app.get("/health")
def health() -> dict:
    """Liveness probe."""
    return {"status": "ok"}


@app.post("/chat")
def chat(message: str = Form(...)) -> dict:
    """Answer `message` using retrieved Summitline context.

    Expected response shape:

        {
          "reply":   "<model response with [source.md] citations>",
          "sources": ["returns-policy.md", "faq.md", ...]
        }
    """
    # Exercise 3 - Step 1 Start
    raise NotImplementedError("Complete Exercise 3 Step 1")
    # Exercise 3 - Step 1 End
