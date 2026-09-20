"""Halcyon policy-retrieval agent — Foundry agent grounded on the Foundry IQ index.

Complete the TODO markers as you work through Lesson 8.
"""
from __future__ import annotations
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model = os.environ["FOUNDRY_MODEL"]
    index_name = os.environ["FOUNDRY_IQ_INDEX"]

    # TODO (Ex 3): instantiate AIProjectClient.
    client: AIProjectClient = ...  # type: ignore[assignment]

    # TODO (Ex 3): build an IQ tool source pointing at the halcyon-policies index.
    # Attach it to the agent's tool list. Signature varies by azure-ai-projects
    # release — refer to the lab agent's cheat sheet for the current shape.

    # TODO (Ex 3): build PromptAgentDefinition — system prompt should tell the agent
    # to always ground answers in the retrieved policy documents and cite the policy
    # name in every answer.
    definition: PromptAgentDefinition = ...  # type: ignore[assignment]

    # TODO (Ex 4): create the agent and send these test questions:
    grounded_questions = [
        "What is the deductible on Halcyon Umbrella Gold?",
        "Does Halcyon Property Basic cover water damage from a burst pipe?",
        "What is the personal-injury coverage limit on Halcyon Umbrella Platinum?",
        "What optional riders does Halcyon Auto Silver support?",
    ]

    for q in grounded_questions:
        print(f"\n=== [GROUNDED] {q} ===")
        # TODO — send q to the agent, print the response with citations.

    # TODO (Ex 5): repeat one of the same questions WITHOUT the IQ tool attached.
    # Compare — the ungrounded run typically invents a plausible-sounding but wrong
    # number. This is the point of the exercise.
    print("\n=== [UNGROUNDED — same question, no IQ] ===")
    # TODO — build a second agent WITHOUT the IQ tool, send the same first question,
    # print the response, and note the divergence.


if __name__ == "__main__":
    main()
