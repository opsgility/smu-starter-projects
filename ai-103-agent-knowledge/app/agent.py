"""Summitline Outfitters concierge agent — Lesson 9 Knowledge Tools lab.

Across three exercises the student assembles three tools onto one agent:

  - Exercise 1 (3388): FileSearchTool over a vector store built from
    sample_data/product-catalog.pdf.
  - Exercise 2 (3389): AzureAISearchTool bound to a Foundry project
    connection that targets the summitline-kb Search index.
  - Exercise 3 (3390): FunctionTool wrapping the custom extract_invoice()
    Content Understanding helper in app/cu_tool.py.

Run with:  python -m app.agent
"""

from __future__ import annotations

import os

from azure.ai.agents.models import (
    AzureAISearchQueryType,
    AzureAISearchTool,
    FilePurpose,
    FileSearchTool,
    FunctionTool,
    ListSortOrder,
    MessageRole,
    ToolSet,
)
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from app.cu_tool import extract_invoice

load_dotenv()

# --- Environment ------------------------------------------------------------

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]
MODEL = os.environ.get("MODEL_DEPLOYMENT_NAME", "gpt-4.1-mini")
SEARCH_CONN = os.environ.get("AZURE_SEARCH_CONNECTION_ID", "")
SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX_NAME", "summitline-kb")


def build_agent_with_tools():
    """Assemble the Summitline concierge agent with all three knowledge tools.

    Returns a (client, agent) tuple. The caller is responsible for creating
    threads, posting messages, and running the agent.
    """
    credential = DefaultAzureCredential()
    client = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential).agents

    # TODO (Exercise 1, Step 6): Upload sample_data/product-catalog.pdf with
    # client.files.upload_and_poll(..., purpose=FilePurpose.AGENTS).
    # Assign the result to a variable named `catalog`.

    # TODO (Exercise 1, Step 6): Create a vector store from [catalog.id] using
    # client.vector_stores.create_and_poll(...). Name it "summitline-catalog".
    # Assign the result to a variable named `vector_store` and assert that
    # vector_store.status == "completed".

    # TODO (Exercise 1, Step 7): Build a FileSearchTool bound to
    # [vector_store.id] and assign it to `file_search`.

    # TODO (Exercise 2, Step 5): Build an AzureAISearchTool using
    # index_connection_id=SEARCH_CONN, index_name=SEARCH_INDEX,
    # query_type=AzureAISearchQueryType.SEMANTIC, top_k=5.
    # Assign it to `ai_search`.

    # TODO (Exercise 3, Step 2): Build a FunctionTool wrapping
    # {extract_invoice} and assign it to `cu_tool`.

    # TODO (Exercise 1, Step 8 -> Exercise 2, Step 6 -> Exercise 3, Step 2):
    # Create a ToolSet and add file_search (Ex1), ai_search (Ex2), and
    # cu_tool (Ex3) to it as you progress through the exercises.
    toolset = ToolSet()

    # TODO (Exercise 3, Step 2): enable the auto function-call loop
    # client.enable_auto_function_calls(toolset)

    # TODO (Exercise 1, Step 8): Create the agent with
    #   model=MODEL,
    #   name="summitline-concierge",
    #   instructions=<see exercise - widen in Ex2 and Ex3>,
    #   tools=toolset.definitions,
    #   tool_resources=toolset.resources,
    # and return (client, agent).
    raise NotImplementedError(
        "Implement build_agent_with_tools() following exercises 1-3."
    )


def ask(client, agent, question: str) -> None:
    """Create a thread, post one question, run the agent, print the reply."""
    thread = client.threads.create()
    client.messages.create(thread_id=thread.id, role=MessageRole.USER, content=question)

    run = client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    if run.status == "failed":
        print(f"[run failed] {run.last_error}")
        return

    messages = list(
        client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    )
    assistant_messages = [m for m in messages if m.role == MessageRole.AGENT]
    if not assistant_messages:
        print("[no assistant response]")
        return

    last = assistant_messages[-1]
    text = last.text_messages[-1].text.value if last.text_messages else ""
    annotations = last.text_messages[-1].text.annotations if last.text_messages else []

    print(f"Q: {question}")
    print(f"A: {text}")
    if annotations:
        print(f"   citations: {annotations}")
    print("-" * 60)


def main() -> None:
    client, agent = build_agent_with_tools()

    try:
        # Exercise 1 only wires file_search, so only the first question will
        # be grounded. Exercise 2 adds the KB/policy question. Exercise 3
        # adds the invoice question.
        for q in [
            "What products do we sell?",
            "What is our return policy for seasonal apparel?",
            "Summarize the invoice in sample_data/invoice.pdf.",
        ]:
            ask(client, agent, q)
    finally:
        # Tidy up the agent so repeat runs don't create duplicates.
        client.delete_agent(agent.id)


if __name__ == "__main__":
    main()
