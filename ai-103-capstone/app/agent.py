"""Capstone agent — Agent Service with file search + AI Search + custom function tool."""
import json
import os

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import (
    AzureAISearchQueryType,
    AzureAISearchTool,
    FunctionTool,
    ListSortOrder,
    ToolSet,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

PROJECT = os.environ["PROJECT_ENDPOINT"]
MODEL = os.environ["MODEL_DEPLOYMENT_NAME"]
SEARCH_CONN = os.environ["AZURE_SEARCH_CONNECTION_ID"]
SEARCH_INDEX = os.environ["AZURE_SEARCH_INDEX"]


def _ship_status(order_id: str) -> str:
    """Look up the shipping status of an order.

    :param order_id: e.g. "ORD-1234"
    """
    return json.dumps({"order_id": order_id, "status": "in transit", "eta_days": 3})


def run(message: str) -> str:
    client = AgentsClient(endpoint=PROJECT, credential=DefaultAzureCredential())
    with client:
        ai_search = AzureAISearchTool(
            index_connection_id=SEARCH_CONN,
            index_name=SEARCH_INDEX,
            query_type=AzureAISearchQueryType.SEMANTIC,
            top_k=5,
        )
        toolset = ToolSet()
        toolset.add(ai_search)
        toolset.add(FunctionTool({_ship_status}))
        client.enable_auto_function_calls(toolset)

        # TODO 1: agent = client.create_agent(model=MODEL, name="capstone-concierge",
        #             instructions="Use search for product/policy questions. Use _ship_status for orders.",
        #             tools=toolset.definitions, tool_resources=toolset.resources).
        # TODO 2: thread = client.threads.create(); send message; create_and_process.
        # TODO 3: Pull last message text. Delete agent. Return text.
        raise NotImplementedError
