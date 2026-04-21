"""FastAPI entrypoint for the Summitline Outfitters multi-agent concierge.

Flow at process startup (ORDER MATTERS):

1. ``load_dotenv()`` — populate env vars from ``.env``.
2. ``tracing.init()`` — configure Azure Monitor OTel BEFORE the FastAPI app is
   constructed. Auto-instrumentation hooks FastAPI middleware at construction
   time; configuring OTel later misses the hook and requests never appear as
   parent spans.
3. ``app = FastAPI(lifespan=...)`` — the lifespan context handles per-process
   agent creation (``build()``) and cleanup (delete orchestrator + workers).

Endpoints
---------
- ``POST /request``             — ask the concierge a question or request a refund.
- ``GET  /approvals``           — list pending HITL approvals.
- ``POST /approvals/{id}``      — approve or deny a pending refund.

Exercises
---------
* Exercise 3392, Steps 3 + 4 — implement ``/request``, ``/approvals``, ``/approvals/{id}``.
* Exercise 3393, Step 4 — confirm ``tracing.init()`` runs before ``FastAPI()``.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from dotenv import load_dotenv

# Step 1: load .env first so APPLICATIONINSIGHTS_CONNECTION_STRING /
# PROJECT_ENDPOINT / MODEL_DEPLOYMENT_NAME are available to everything below.
load_dotenv()

# Step 2: initialize Azure Monitor OTel BEFORE FastAPI is imported/constructed.
# Exercise 3393 replaces the NotImplementedError in tracing.init() with the
# real configure_azure_monitor call.
from app import tracing  # noqa: E402  (must follow load_dotenv)

_tracer = tracing.init()

# Step 3: now it is safe to import + construct FastAPI.
from fastapi import FastAPI, Form  # noqa: E402

from app.orchestrator import build  # noqa: E402
from app.worker import FUTURES, PENDING, converse  # noqa: E402

# Shared state populated by the lifespan context below.
_client = None
_orchestrator = None
_worker_ids: list[str] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create the orchestrator + workers on startup, delete them on shutdown."""
    global _client, _orchestrator, _worker_ids
    _client, _orchestrator, _worker_ids = build()
    try:
        yield
    finally:
        # Best-effort cleanup. Delete workers first, then the orchestrator, then
        # close the shared AgentsClient so its connection pool is released.
        if _client is not None:
            for agent_id in _worker_ids:
                try:
                    _client.delete_agent(agent_id)
                except Exception:
                    pass
            if _orchestrator is not None:
                try:
                    _client.delete_agent(_orchestrator.id)
                except Exception:
                    pass
            try:
                _client.close()
            except Exception:
                pass


app = FastAPI(title="Summitline Multi-Agent Concierge", lifespan=lifespan)


@app.post("/request")
def request(message: str = Form(...), customer_id: str = Form("anonymous")) -> dict:
    """Forward a user message to the orchestrator and return its final reply.

    Wrap the orchestrator call in a ``handle_request`` span so Application
    Insights shows one end-to-end transaction per ``/request`` (parent) with
    agent runs + tool calls as child dependencies.

    Span attributes to attach (Exercise 3393, Step 7 verification):
    - ``summitline.customer_id``     — the ``customer_id`` form field.
    - ``summitline.message_length``  — ``len(message)``.
    - ``summitline.status``          — ``"ok"`` (or ``"error"`` on failure).
    """
    # TODO (Exercise 3392 Step 3): open a span named "handle_request" via
    # _tracer.start_as_current_span, set the three summitline.* attributes,
    # call converse(_client, _orchestrator, message), and return {"reply": reply}.
    raise NotImplementedError("Exercise 3392 Step 3: implement POST /request")


@app.get("/approvals")
def list_approvals():
    """Return every pending HITL approval currently blocking a refund."""
    # TODO (Exercise 3392 Step 4): return [{"id": k, **v} for k, v in PENDING.items() if v["status"] == "pending"].
    raise NotImplementedError("Exercise 3392 Step 4: implement GET /approvals")


@app.post("/approvals/{approval_id}")
def resolve(approval_id: str, decision: str = Form(...)):
    """Resolve a pending refund approval.

    ``decision`` must be ``"approved"`` or ``"denied"``. Setting the Future
    result unblocks the ``request_refund`` call that is waiting inside the
    refund worker's tool invocation.
    """
    # TODO (Exercise 3392 Step 4): if approval_id not in FUTURES, return an error dict.
    # Otherwise, update PENDING[approval_id]["status"] = decision,
    # call FUTURES[approval_id].set_result(decision), and return {"ok": True, "decision": decision}.
    raise NotImplementedError("Exercise 3392 Step 4: implement POST /approvals/{id}")
