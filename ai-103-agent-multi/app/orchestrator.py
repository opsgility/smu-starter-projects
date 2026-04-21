"""Orchestrator agent for the Summitline Outfitters multi-agent concierge.

The orchestrator (``summitline-concierge``) delegates to the two worker agents
via ``ConnectedAgentTool``:

- ``lookup_worker`` — read-only Summitline order lookup.
- ``refund_worker`` — refund issuance (behind a Python-enforced HITL gate).

The orchestrator's instructions encode the Summitline policy that refunds must
never fire before a lookup has verified the order exists. The tool descriptions
repeat that rule to give the model a second layer of guidance (layered defense).

Exercises
---------
* Exercise 3392, Step 1 — implement ``build()``.
"""

from __future__ import annotations

import os
from typing import List, Tuple

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import ConnectedAgentTool
from azure.identity import DefaultAzureCredential

from app.worker import make_lookup_worker, make_refund_worker

# Environment-variable contract — set by .env (see .env.example).
ENDPOINT: str = os.environ.get("PROJECT_ENDPOINT", "")
MODEL: str = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4.1")


def build() -> Tuple[AgentsClient, object, List[str]]:
    """Build the Summitline multi-agent system.

    Returns a tuple of:
    - ``client`` — the shared ``AgentsClient`` (callers must close it on shutdown).
    - ``orchestrator`` — the ``summitline-concierge`` supervisor agent.
    - ``worker_ids`` — ids of the created workers, so ``main.py`` can delete them
      when the FastAPI lifespan shuts down.

    Implementation must:
    1. Construct ``AgentsClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())``.
    2. Call ``make_refund_worker(client, MODEL)`` and ``make_lookup_worker(client, MODEL)``.
    3. Wrap each worker in a ``ConnectedAgentTool`` with ``id=<agent>.id`` (NOT the name).
    4. Create the orchestrator agent named ``"summitline-concierge"`` with combined
       tool definitions (``refund_tool.definitions + lookup_tool.definitions``) and
       instructions that tell it to call ``lookup_worker`` before ``refund_worker``.
    5. Return ``(client, orchestrator, [refund_agent.id, lookup_agent.id])``.
    """
    # TODO (Exercise 3392 Step 1): implement build() per the docstring above.
    # Pay attention to:
    #   - ConnectedAgentTool(id=..., name=..., description=...) — id must be the
    #     GUID from the returned agent object, not the agent name string.
    #   - tools=refund_tool.definitions + lookup_tool.definitions (list concat).
    #   - instructions must tell the orchestrator to verify with lookup_worker
    #     before calling refund_worker, and to summarize tool output in one
    #     sentence for the end user.
    raise NotImplementedError("Exercise 3392 Step 1: implement orchestrator.build()")
