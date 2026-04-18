"""Build a concierge agent with three function tools and run a thread."""
import os

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FunctionTool, ListSortOrder, ToolSet
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from .functions import USER_FUNCTIONS

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
MODEL = os.environ["MODEL_DEPLOYMENT_NAME"]

INSTRUCTIONS = (
    "You are the Northwind Horizon concierge. Use the tools available to you to answer "
    "questions about weather, simple calculations, and product inventory. Always cite "
    "the tool you used in your final reply."
)


def build_client() -> AgentsClient:
    return AgentsClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())


def converse(messages: list[str]) -> list[dict]:
    """Run a single conversation through a fresh agent + thread."""
    with build_client() as client:
        # TODO 1: Build ToolSet, add FunctionTool(USER_FUNCTIONS), enable auto function calls
        #         via client.enable_auto_function_calls(toolset).
        # TODO 2: agent = client.create_agent(model=MODEL, name="northwind-concierge",
        #             instructions=INSTRUCTIONS, tools=toolset.definitions,
        #             tool_resources=toolset.resources)
        # TODO 3: thread = client.threads.create()
        # TODO 4: For each message in `messages`:
        #             client.messages.create(thread_id=thread.id, role="user", content=message)
        #             client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
        # TODO 5: Pull the conversation: msgs = client.messages.list(thread_id=thread.id,
        #             order=ListSortOrder.ASCENDING). Convert to [{"role":m.role, "text":m.text_messages[-1].text.value}]
        #             when text_messages is non-empty.
        # TODO 6: client.delete_agent(agent.id) before returning. Return the converted list.
        raise NotImplementedError
