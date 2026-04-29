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

    # Exercise 1 - Step 6 Start
    raise NotImplementedError("Complete Exercise 1 Step 6, then continue with Exercises 2 and 3")
    # Exercise 1 - Step 6 End


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
