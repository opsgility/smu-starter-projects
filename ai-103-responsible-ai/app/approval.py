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
    """Queue a new approval request and return its id."""
    # Exercise 3 - Step 1 Start
    raise NotImplementedError("Complete Exercise 3 Step 1")
    # Exercise 3 - Step 1 End


def list_pending() -> list[ApprovalRequest]:
    """Return every request still in `pending` status."""
    # Exercise 3 - Step 1 Start
    raise NotImplementedError("Complete Exercise 3 Step 1")
    # Exercise 3 - Step 1 End


def decide(req_id: str, approved: bool, reason: str = "") -> ApprovalRequest:
    """Approve or reject a pending request and return the updated record."""
    # Exercise 3 - Step 1 Start
    raise NotImplementedError("Complete Exercise 3 Step 1")
    # Exercise 3 - Step 1 End
