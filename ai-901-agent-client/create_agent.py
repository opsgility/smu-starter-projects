"""
(Optional) Create a single-agent solution programmatically via the Foundry SDK.
In the lab the default path is the Foundry portal — use this script if you
prefer code-first.
"""
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

ENDPOINT = os.environ["PROJECT_ENDPOINT"]
MODEL = os.environ.get("MODEL_DEPLOYMENT_NAME", "ai901-chat")


def create() -> str:
    project = AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())

    # TODO 1: call project.agents.create_agent(
    #             model=MODEL,
    #             name="Northwind Concierge",
    #             instructions="You help Northwind Horizon shoppers find gifts and answer policy questions.",
    #             tools=[]
    #         )
    # TODO 2: return agent.id
    raise NotImplementedError


if __name__ == "__main__":
    agent_id = create()
    print(f"AGENT_ID={agent_id}")
    print("Save this value to your .env file.")
