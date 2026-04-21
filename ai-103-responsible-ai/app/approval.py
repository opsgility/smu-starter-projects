"""In-memory approval queue for human-in-the-loop gating.

Exercise 3 (Lab 2263) — implement submit(), list_pending(), and decide() backed
by a `dict` and a `threading.Lock`. Production replaces this with Service Bus,
Azure Storage Queue, or Cosmos DB so uvicorn restarts don't lose pending work.
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
    """Queue a new approval request and return its id.

    TODO (Exercise 3 Step 1): build an ApprovalRequest, store it in _queue
    under the lock, and return req.id.
    """
    # TODO (Exercise 3 Step 1): create the ApprovalRequest and store under `_lock`.
    raise NotImplementedError("Implement approval.submit() in Exercise 3, Step 1.")


def list_pending() -> list[ApprovalRequest]:
    """Return every request still in `pending` status.

    TODO (Exercise 3 Step 1): take the lock and return a list comprehension
    over _queue.values() filtering on status == "pending".
    """
    # TODO (Exercise 3 Step 1): return pending requests under `_lock`.
    raise NotImplementedError("Implement approval.list_pending() in Exercise 3, Step 1.")


def decide(req_id: str, approved: bool, reason: str = "") -> ApprovalRequest:
    """Approve or reject a pending request and return the updated record.

    TODO (Exercise 3 Step 1): under the lock, look up req_id in _queue. Raise
    ValueError if the request is not pending (idempotency). Otherwise set
    req.status to "approved"/"rejected" and req.reason, then return req.
    """
    # TODO (Exercise 3 Step 1): update status/reason under `_lock`. Raise
    # ValueError if req.status != "pending". KeyError propagates naturally if
    # req_id is not in the queue.
    raise NotImplementedError("Implement approval.decide() in Exercise 3, Step 1.")
