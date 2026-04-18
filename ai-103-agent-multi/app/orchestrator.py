"""Orchestrator agent that delegates to refund / lookup workers via the connected-agent tool."""
import os

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import ConnectedAgentTool, ListSortOrder
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from .worker import make_lookup_worker, make_refund_worker

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
MODEL = os.environ["MODEL_DEPLOYMENT_NAME"]


def build():
    client = AgentsClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())

    refund_agent = make_refund_worker(client, MODEL)
    lookup_agent = make_lookup_worker(client, MODEL)

    # TODO 1: Build two ConnectedAgentTool wrappers — one per worker:
    #         refund_tool = ConnectedAgentTool(id=refund_agent.id, name="refund_worker",
    #                                            description="Use to issue refunds.")
    # TODO 2: Combine the two tool definitions into a list and create the orchestrator:
    #         orchestrator = client.create_agent(model=MODEL, name="northwind-orchestrator",
    #             instructions="Delegate refunds to refund_worker and lookups to lookup_worker. "
    #                          "Never call refund_worker without first calling lookup_worker to "
    #                          "verify the order.",
    #             tools=refund_tool.definitions + lookup_tool.definitions)
    # TODO 3: Return (client, orchestrator, [refund_agent.id, lookup_agent.id]) so the caller
    #         can clean them up.
    raise NotImplementedError


def converse(client, orchestrator, user_message: str) -> str:
    thread = client.threads.create()
    client.messages.create(thread_id=thread.id, role="user", content=user_message)
    client.runs.create_and_process(thread_id=thread.id, agent_id=orchestrator.id)
    msgs = list(client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING))
    return msgs[-1].text_messages[-1].text.value if msgs and msgs[-1].text_messages else ""
