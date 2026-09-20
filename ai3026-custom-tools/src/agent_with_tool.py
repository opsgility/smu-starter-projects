"""Halcyon adjuster claim-drafter agent with a `lookup_policy_summary` FunctionTool.

Complete the TODO markers as you work through Lesson 4. Every TODO maps to a specific
exercise step in the lab pane.
"""
from __future__ import annotations
import json
import os
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FunctionTool, PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "halcyon-policies.json"


def load_policies() -> dict[str, dict]:
    """Load the 6 fictional Halcyon policies from disk into a dict keyed by policy_number."""
    with DATA_FILE.open() as fh:
        records = json.load(fh)
    return {r["policy_number"]: r for r in records}


POLICIES = load_policies()


# TODO (Ex 2): implement `lookup_policy_summary` — the function the agent will call.
# The docstring becomes the tool description the LLM sees; the signature becomes the tool
# schema. Return a dict with deductible / coverage_limits / riders / active status. Return
# a {"error": "..."} shape when the policy isn't in the dict.
def lookup_policy_summary(policy_number: str) -> dict:
    """Look up a Halcyon policy by policy number and return its summary.

    Args:
        policy_number: The Halcyon policy number, e.g. "HAL-UMB-GOLD-000123".

    Returns:
        A dict with deductible, coverage_limits, riders, and active status.
    """
    # TODO — return POLICIES.get(policy_number) with a sensible error shape when missing.
    raise NotImplementedError("Complete this in Lesson 4 Exercise 2.")


def main() -> None:
    load_dotenv()
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    model = os.environ["FOUNDRY_MODEL"]

    # TODO (Ex 3): instantiate AIProjectClient with DefaultAzureCredential.
    client: AIProjectClient = ...  # type: ignore[assignment]

    # TODO (Ex 3): register `lookup_policy_summary` as a FunctionTool.
    tool: FunctionTool = ...  # type: ignore[assignment]

    # TODO (Ex 3): build a PromptAgentDefinition — this becomes the Halcyon adjuster
    # claim-drafter agent. System prompt should tell the agent to (1) call
    # lookup_policy_summary when the user mentions a policy number and (2) draft a
    # first-response paragraph citing deductible + coverage.
    definition: PromptAgentDefinition = ...  # type: ignore[assignment]

    # TODO (Ex 4): create the agent + a thread + a message + a run. Print the final
    # response for each of these three test claims:
    test_claims = [
        "Claim from policy HAL-UMB-GOLD-000123: kitchen fire, sprinkler damage to the ceiling.",
        "Claim from policy HAL-AUTO-SIL-000456: rear-ended in stop-and-go traffic on I-35.",
        "Claim from an unknown policy number: rider hit a mailbox with my truck.",
    ]

    for claim in test_claims:
        print(f"\n===\n{claim}\n===")
        # TODO — send `claim` to the agent, print the final text response.


if __name__ == "__main__":
    main()
