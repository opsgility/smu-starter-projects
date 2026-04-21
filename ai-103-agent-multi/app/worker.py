"""Worker agents for the Summitline Outfitters multi-agent concierge.

This module defines two focused worker agents plus their Python-side helpers:

- ``refund_worker``  — single ``FunctionTool`` wrapping ``_refund``.
- ``lookup_worker`` — single ``FunctionTool`` wrapping ``_lookup_order``.

The human-in-the-loop (HITL) approval gate for refunds over $100 lives in
``request_refund`` (Python code — not the agent's natural-language instructions)
so prompt injection cannot bypass it. Pending approvals and the futures the
worker blocks on are held in module-level ``PENDING`` and ``FUTURES`` dicts so
``app/main.py`` can inspect and resolve them from FastAPI endpoints.

Exercises
---------
* Exercise 3391, Step 7 — implement ``make_refund_worker``.
* Exercise 3391, Step 8 — implement ``make_lookup_worker``.
* Exercise 3392, Step 2 — HITL gate is already implemented below as the
  reference pattern; students study/extend it.
"""

from __future__ import annotations

import asyncio
import uuid
from typing import Any, Dict

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FunctionTool, ToolSet

# ---------------------------------------------------------------------------
# Module-level state for the HITL approval queue.
#
# PENDING: approval_id -> {"order_id": str, "amount": float, "status": str}
# FUTURES: approval_id -> asyncio.Future (resolved with "approved" or "denied")
#
# In production these should live in Cosmos DB or Service Bus so a restart
# doesn't drop pending refunds on the floor. In-memory is fine for the lab.
# ---------------------------------------------------------------------------
PENDING: Dict[str, Dict[str, Any]] = {}
FUTURES: Dict[str, asyncio.Future] = {}


# ---------------------------------------------------------------------------
# Business-logic helpers (FULLY IMPLEMENTED — students do not fill these in).
# ---------------------------------------------------------------------------

def request_refund(order_id: str, amount: float) -> dict:
    """Process a Summitline refund. Amounts over $100 require human approval.

    The $100 threshold lives in Python on purpose — prompt injection can talk
    a model out of following its instructions, but it cannot talk Python out
    of an ``if`` branch.

    :param order_id: Summitline order ID.
    :param amount: Refund amount in USD.
    :return: dict with status ('refunded' | 'denied' | 'timeout') and order_id.
    """
    if amount <= 100:
        return {"status": "refunded", "order_id": order_id, "amount": amount}

    approval_id = str(uuid.uuid4())
    fut = asyncio.get_event_loop().create_future()
    FUTURES[approval_id] = fut
    PENDING[approval_id] = {
        "order_id": order_id,
        "amount": amount,
        "status": "pending",
    }
    try:
        decision = asyncio.get_event_loop().run_until_complete(
            asyncio.wait_for(fut, timeout=300)
        )
    except asyncio.TimeoutError:
        return {"status": "timeout", "order_id": order_id}
    return {
        "status": "refunded" if decision == "approved" else "denied",
        "order_id": order_id,
    }


def _refund(order_id: str, amount: float, reason: str) -> dict:
    """Issue a Summitline refund for an order.

    This is the function the refund worker's FunctionTool wraps. It delegates
    to ``request_refund`` so the HITL gate is enforced before the refund is
    actually booked.

    :param order_id: Summitline order ID (e.g. "ORD-1234").
    :param amount: Refund amount in USD.
    :param reason: Short human-readable reason for the refund.
    :return: dict with status, order_id, and (on success) amount.
    """
    result = request_refund(order_id=order_id, amount=amount)
    result["reason"] = reason
    return result


def _lookup_order(order_id: str) -> dict:
    """Look up the current status of a Summitline order.

    Read-only by design — the lookup worker has no other tools, so it cannot
    mutate state even if its prompt is compromised.

    :param order_id: Summitline order ID (e.g. "ORD-1234").
    :return: dict describing the order.
    """
    # Deterministic stub data for the lab. A real implementation would call
    # the Summitline order-management API.
    return {
        "order_id": order_id,
        "status": "shipped",
        "total": 49.99,
        "currency": "USD",
        "tracking_number": "1Z999AA10123456784",
    }


# ---------------------------------------------------------------------------
# Conversation helper — used by the FastAPI /request endpoint to drive the
# orchestrator through one turn and return its final reply text.
# ---------------------------------------------------------------------------

def converse(client: AgentsClient, orchestrator, message: str) -> str:
    """Run one user turn through the orchestrator and return its final reply.

    Creates a fresh thread, posts the user message, processes the run (which
    may fan out to connected workers + tool calls), and returns the last
    assistant text message.

    :param client: Shared ``AgentsClient`` used to create threads and runs.
    :param orchestrator: The orchestrator agent returned by ``build()``.
    :param message: The end-user message to forward to the orchestrator.
    :return: The orchestrator's final assistant reply (or a diagnostic string).
    """
    from azure.ai.agents.models import ListSortOrder  # local import to keep top clean

    thread = client.threads.create()
    client.messages.create(thread_id=thread.id, role="user", content=message)
    client.runs.create_and_process(thread_id=thread.id, agent_id=orchestrator.id)

    last_reply = ""
    for m in client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING):
        if m.role == "assistant" and m.text_messages:
            last_reply = m.text_messages[-1].text.value
    return last_reply or "(no reply)"


# ---------------------------------------------------------------------------
# Worker factories — students implement these.
# ---------------------------------------------------------------------------

def make_refund_worker(client: AgentsClient, model: str):
    """Create the ``refund-worker`` agent with a single ``_refund`` tool.

    The worker must:
    - Register ``_refund`` as a ``FunctionTool`` in a ``ToolSet``.
    - Call ``client.enable_auto_function_calls(toolset)`` BEFORE ``create_agent``
      so the shared client auto-invokes the Python function when the model
      emits a tool call.
    - Create an agent named ``"refund-worker"`` bound to ``model`` with
      instructions that restrict it to issuing Summitline refunds.
    - Return the agent object so the caller can reuse ``agent.id`` with
      ``ConnectedAgentTool``.
    """
    # TODO (Exercise 3391 Step 7): Build a ToolSet containing FunctionTool({_refund}),
    # call client.enable_auto_function_calls(toolset), and return
    # client.create_agent(model=model, name="refund-worker", instructions=..., tools=toolset.definitions, tool_resources=toolset.resources).
    raise NotImplementedError("Exercise 3391 Step 7: implement make_refund_worker")


def make_lookup_worker(client: AgentsClient, model: str):
    """Create the ``lookup-worker`` agent with a single ``_lookup_order`` tool.

    Mirrors ``make_refund_worker`` but registers ``_lookup_order`` and uses
    read-only instructions. Keeping reads and writes on separate workers lets
    you attach different RBAC, rate limits, and routing policy (see Exercise
    3392).
    """
    # TODO (Exercise 3391 Step 8): Build a ToolSet containing FunctionTool({_lookup_order}),
    # call client.enable_auto_function_calls(toolset), and return
    # client.create_agent(model=model, name="lookup-worker", instructions=..., tools=toolset.definitions, tool_resources=toolset.resources).
    raise NotImplementedError("Exercise 3391 Step 8: implement make_lookup_worker")
