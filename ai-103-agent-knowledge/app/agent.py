"""Agent with file search + Azure AI Search + Content Understanding tools."""
import os

from azure.ai.agents import AgentsClient
from azure.ai.agents.models import (
    AzureAISearchQueryType,
    AzureAISearchTool,
    FilePurpose,
    FileSearchTool,
    FunctionTool,
    ListSortOrder,
    ToolSet,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from .cu_tool import extract_invoice

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
MODEL = os.environ["MODEL_DEPLOYMENT_NAME"]
SEARCH_CONN = os.environ["AZURE_SEARCH_CONNECTION_ID"]
SEARCH_INDEX = os.environ["AZURE_SEARCH_INDEX_NAME"]


def build_agent_with_tools():
    client = AgentsClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())

    # TODO 1: Upload sample_data/product-catalog.pdf via
    #         client.files.upload_and_poll(file_path=..., purpose=FilePurpose.AGENTS).
    # TODO 2: Create a vector store: client.vector_stores.create_and_poll(file_ids=[file.id],
    #         name="product-catalog").
    # TODO 3: Build FileSearchTool(vector_store_ids=[vs.id]).
    # TODO 4: Build AzureAISearchTool(index_connection_id=SEARCH_CONN, index_name=SEARCH_INDEX,
    #         query_type=AzureAISearchQueryType.SEMANTIC, top_k=5).
    # TODO 5: Build FunctionTool({extract_invoice}).
    # TODO 6: Combine in a ToolSet, then client.create_agent(model=MODEL,
    #         name="northwind-knowledge", instructions="...",
    #         tools=toolset.definitions, tool_resources=toolset.resources).
    raise NotImplementedError


def main():
    client, agent = build_agent_with_tools()
    with client:
        thread = client.threads.create()
        for q in ["What products do we sell?", "Summarize the invoice in sample_data/invoice.pdf."]:
            client.messages.create(thread_id=thread.id, role="user", content=q)
            client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
        for m in client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING):
            if m.text_messages:
                print(f"{m.role:9} | {m.text_messages[-1].text.value}")
        client.delete_agent(agent.id)


if __name__ == "__main__":
    main()
