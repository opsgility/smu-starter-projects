"""Northwind capstone API.

POST /ask -> RAG retrieval against Cosmos vectors, calls Azure OpenAI for answer,
            and publishes a "question-answered" event onto Service Bus for downstream.

The student wires together steps that exist in prior modules:
  Step 5 — finish the /ask handler (TODO marker)
  Step 6 — emit a Service Bus event when an answer is generated (TODO marker)
"""
from __future__ import annotations

import logging
import os

from fastapi import FastAPI
from pydantic import BaseModel

from lib.cosmos_vector import search
from lib.embeddings import chat, embed
from lib.sb_producer import send_to_queue
from lib.telemetry import tracer

_t = tracer()
app = FastAPI(title="Northwind Capstone API", version="1.0.0")
log = logging.getLogger("northwind")


class AskRequest(BaseModel):
    tenant: str
    question: str


class AskResponse(BaseModel):
    answer: str
    hits: list[dict]


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest) -> AskResponse:
    with _t.start_as_current_span("ask") as span:
        span.set_attribute("tenant", req.tenant)

        # TODO(step5): replace the three lines below to implement:
        #   1. qv = embed(req.question)
        #   2. hits = search(qv, tenant=req.tenant, top_k=5)
        #   3. context = [h["text"] for h in hits]
        #   4. answer = chat(req.question, context)
        # (Keep the span.set_attribute calls; just replace the raise NotImplementedError.)
        raise NotImplementedError("Step 5: implement /ask")
        # span.set_attribute("hits", len(hits))
        # log.info("answered tenant=%s hits=%d", req.tenant, len(hits))

        # TODO(step6): after generating `answer`, emit a Service Bus event:
        #   send_to_queue(
        #       "northwind-events",
        #       {"event": "question.answered", "tenant": req.tenant,
        #        "question": req.question, "hits": len(hits)},
        #   )

        # return AskResponse(answer=answer, hits=hits)
