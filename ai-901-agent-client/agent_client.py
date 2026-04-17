"""
Single-agent client — talk to an agent created in Foundry.

Steps:
1. Create a thread.
2. Add a user message to the thread.
3. Start a run against the agent.
4. Poll the run until terminal status.
5. Fetch the last assistant message and print it.
"""
import os
import time

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
AGENT_ID = os.environ["AGENT_ID"]


def ask(user_text: str) -> str:
    project = AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())
    agents = project.agents

    # TODO 1: create a thread -> thread = agents.threads.create()
    # TODO 2: add a user message   -> agents.messages.create(thread_id=thread.id, role="user", content=user_text)
    # TODO 3: start a run          -> run = agents.runs.create(thread_id=thread.id, agent_id=AGENT_ID)
    # TODO 4: poll run status until it's "completed", "failed", or "cancelled".
    #         Sleep briefly between polls.
    # TODO 5: list messages on the thread, find the latest assistant message,
    #         return its text content.
    raise NotImplementedError


if __name__ == "__main__":
    print(ask("I need a birthday gift for my nephew who loves Legos."))
