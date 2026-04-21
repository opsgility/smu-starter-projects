"""FastAPI surface for the Summitline Outfitters retrieval pipeline.

Exposes two endpoints on top of `pipeline.query`:

  GET  /search?q=...           -> hybrid retrieval hits (no generation)
  POST /chat  {"question": ...} -> grounded answer + citations via cite()

Run locally:
    uvicorn app.main:app --reload --port 8000
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from pipeline import query as query_module

app = FastAPI(
    title="Summitline Outfitters Knowledge API",
    description="Hybrid retrieval + grounded citations over the "
                "summitline-knowledge AI Search index.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    question: str
    k: int = 5


class ChatResponse(BaseModel):
    answer: str
    citations: list[str]
    invalid_citations: list[str]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/search")
def search(q: str = Query(..., min_length=1), k: int = 5) -> dict:
    """Plain hybrid retrieval - no LLM in the loop."""
    try:
        hits = query_module.query(q, k=k)
    except Exception as exc:  # surface exception text during the lab
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return {"query": q, "k": k, "hits": hits}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """Grounded answer - invokes pipeline.query.cite()."""
    try:
        result = query_module.cite(req.question, k=req.k)
    except NotImplementedError as exc:
        raise HTTPException(
            status_code=501,
            detail="cite() is not implemented yet (finish Exercise 4).",
        ) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return ChatResponse(**result)
