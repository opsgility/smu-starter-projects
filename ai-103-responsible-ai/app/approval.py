"""In-memory approval queue for human-in-the-loop gating.

This is NOT production-grade — swap for Service Bus / queue storage in a real deployment.
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from typing import Literal

Status = Literal["pending", "approved", "rejected"]


@dataclass
class ApprovalRequest:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prompt: str = ""
    draft_response: str = ""
    status: Status = "pending"
    reason: str = ""


_lock = threading.Lock()
_queue: dict[str, ApprovalRequest] = {}


def submit(prompt: str, draft_response: str) -> str:
    """Add a new approval request and return its id."""
    # TODO 1: construct ApprovalRequest(prompt=prompt, draft_response=draft_response).
    # TODO 2: store it in _queue keyed by req.id under _lock.
    # TODO 3: return req.id.
    raise NotImplementedError


def list_pending() -> list[ApprovalRequest]:
    with _lock:
        return [r for r in _queue.values() if r.status == "pending"]


def decide(req_id: str, approved: bool, reason: str = "") -> ApprovalRequest:
    # TODO 4: under _lock, fetch _queue[req_id]; set status + reason; return the updated record.
    raise NotImplementedError
