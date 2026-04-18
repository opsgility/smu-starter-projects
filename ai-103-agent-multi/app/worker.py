"""Worker agent factories — created at startup, reused per request."""
import json
import os

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FunctionTool, ToolSet


def _refund(order_id: str, reason: str) -> str:
    """Issue a refund for an order.

    :param order_id: e.g. "ORD-1234"
    :param reason: free-text reason
    """
    return json.dumps({"order_id": order_id, "refunded": True, "reason": reason})


def _lookup_order(order_id: str) -> str:
    """Look up an order's status.

    :param order_id: e.g. "ORD-1234"
    """
    sample = {"ORD-1234": {"status": "shipped", "total": 49.99}}
    return json.dumps(sample.get(order_id, {"status": "not found"}))


def make_refund_worker(client: AgentsClient, model: str):
    toolset = ToolSet()
    toolset.add(FunctionTool({_refund}))
    client.enable_auto_function_calls(toolset)
    # TODO 1: client.create_agent(model=model, name="refund-worker",
    #         instructions="You issue refunds. Always confirm order_id and reason.",
    #         tools=toolset.definitions, tool_resources=toolset.resources). Return the agent.
    raise NotImplementedError


def make_lookup_worker(client: AgentsClient, model: str):
    toolset = ToolSet()
    toolset.add(FunctionTool({_lookup_order}))
    client.enable_auto_function_calls(toolset)
    # TODO 2: Same shape as refund worker; instructions = "You look up order details. Read-only."
    raise NotImplementedError
