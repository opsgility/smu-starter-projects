"""FastAPI front-end: /request submits to orchestrator; /approvals manages the queue."""
import threading
import uuid

from fastapi import FastAPI, Form, HTTPException

from . import tracing
from .orchestrator import build, converse

app = FastAPI(title="AI-103 multi-agent + approval starter")
_tracer = tracing.init()
_lock = threading.Lock()
_approvals: dict[str, dict] = {}

# Build orchestrator once at startup (requires _client.close() at shutdown — see TODO 3).
_client, _orchestrator, _worker_ids = build()


@app.post("/request")
def request(message: str = Form(...), requires_approval: bool = Form(False)) -> dict:
    # TODO 1: Open a tracer span: with _tracer.start_as_current_span("request") as span:
    #             span.set_attribute("requires_approval", requires_approval).
    # TODO 2: If requires_approval is False, call converse(_client, _orchestrator, message)
    #         and return {"reply": text}.
    # TODO 3: If requires_approval is True, push {"id": str(uuid.uuid4()), "message": message,
    #         "status": "pending"} into _approvals under _lock and return {"approval_id": id}.
    raise NotImplementedError


@app.get("/approvals")
def list_approvals() -> list:
    with _lock:
        return [r for r in _approvals.values() if r["status"] == "pending"]


@app.post("/approvals/{approval_id}")
def decide(approval_id: str, approved: bool = Form(...)) -> dict:
    with _lock:
        record = _approvals.get(approval_id)
        if not record:
            raise HTTPException(404, detail="approval not found")
        if not approved:
            record["status"] = "rejected"
            return record
    # On approval, run the request through the orchestrator and stash the reply.
    text = converse(_client, _orchestrator, record["message"])
    with _lock:
        record["status"] = "approved"
        record["reply"] = text
        return record


@app.on_event("shutdown")
def shutdown():
    for wid in _worker_ids:
        _client.delete_agent(wid)
    _client.delete_agent(_orchestrator.id)
    _client.close()
