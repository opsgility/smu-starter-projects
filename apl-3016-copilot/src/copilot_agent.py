# Halcyon Assist agent skeleton. Bare-minimum single-turn conversation on the
# Foundry chat deployment, extended lesson by lesson through the course.
from __future__ import annotations

import asyncio
import os
import sys

from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential

from agent_framework import Agent, AgentThread
from agent_framework.foundry import FoundryChatClient


# --- system prompt ---
# Lessons 4 and 8 extend this. Keep the tone customer-safe and the escalation
# rule explicit - the agent should hand off to a licensed adjuster on any
# claims-decision question, and should never quote coverage amounts it cannot
# ground in a retrieved policy document.
SYSTEM_PROMPT = (
    "You are Halcyon Assist, a policy-lookup copilot for Halcyon Insurance "
    "customer-service agents. Answer questions about Halcyon's homeowners, "
    "auto, and umbrella policies in clear, customer-safe language. "
    "Rules:\n"
    " - Never quote a specific coverage amount, deductible, or premium unless "
    "the value appears verbatim in a policy document you have retrieved.\n"
    " - Never make a claims-approval or claims-denial decision. If the user "
    "is asking whether a specific claim will be paid, say so and recommend "
    "they escalate to a licensed Halcyon adjuster.\n"
    " - Keep replies to two or three short paragraphs.\n"
    " - Refer to the company as 'Halcyon Insurance' and to yourself as "
    "'Halcyon Assist'."
)


def require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value or value.startswith("<"):
        print(f"[copilot_agent] Missing env var: set this variable in .env -> {name}")
        sys.exit(1)
    return value


def build_agent() -> Agent:
    """Build the Halcyon Assist agent bound to the Foundry chat deployment."""
    endpoint = require_env("AZURE_AI_PROJECT_ENDPOINT")
    deployment = require_env("AZURE_AI_CHAT_DEPLOYMENT")

    client = FoundryChatClient(
        project_endpoint=endpoint,
        model=deployment,
        credential=DefaultAzureCredential(),
    )
    return Agent(
        client=client,
        name="halcyon-assist",
        instructions=SYSTEM_PROMPT,
    )


# --- run ---
async def run_once(question: str) -> str:
    """Send one question to the agent and return the assistant reply."""
    agent = build_agent()
    thread: AgentThread = agent.get_new_thread()
    result = await agent.run(question, thread=thread)
    return str(result)


# --- streaming ---
async def run_stream(question: str) -> None:
    """Stream the agent's reply token-by-token. Used from Lesson 8 onward."""
    agent = build_agent()
    thread: AgentThread = agent.get_new_thread()
    print("Halcyon Assist: ", end="", flush=True)
    async for chunk in agent.run(question, thread=thread, stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()


async def _main() -> None:
    load_dotenv()
    question = (
        "A customer's fence blew down in a storm. In one paragraph, explain "
        "how Halcyon homeowners coverage typically treats fence damage from "
        "wind, without quoting a specific coverage amount."
    )
    reply = await run_once(question)
    print(f"Halcyon Assist: {reply}")


if __name__ == "__main__":
    asyncio.run(_main())
