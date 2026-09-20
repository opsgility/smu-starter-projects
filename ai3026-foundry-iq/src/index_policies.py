"""Bulk-upload the 4 Halcyon policy .md files into a Foundry IQ vector index.

Idempotent — checks whether the named index already contains each doc and skips
uploads that would be redundant.

Complete the TODO markers as you work through Lesson 8 Exercise 2.
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


POLICY_DIR = Path(__file__).resolve().parents[1] / "policies"


def main() -> int:
    load_dotenv()
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    index_name = os.environ["FOUNDRY_IQ_INDEX"]

    # TODO (Ex 2): instantiate AIProjectClient with DefaultAzureCredential.
    client: AIProjectClient = ...  # type: ignore[assignment]

    # TODO (Ex 2): ensure the Foundry IQ index exists. If not, create it. Refer to
    # the lab agent's cheat sheet for the exact `client.indexes.create_or_update(...)`
    # shape — signature varies slightly across azure-ai-projects releases.

    # Upload each policy file.
    policy_files = sorted(POLICY_DIR.glob("*.md"))
    print(f"[index_policies] found {len(policy_files)} policy file(s)")

    for policy_file in policy_files:
        print(f"[index_policies] uploading {policy_file.name} ...")
        # TODO (Ex 2): upload policy_file.read_text() as a document to the IQ index.
        # Set document.id = policy_file.stem so re-runs are idempotent.

    print("[index_policies] all uploads submitted")

    # TODO (Ex 3): poll the index status until every uploaded doc is 'indexed'.
    # Foundry IQ typically takes 30-60s per doc for embed + shard + persist.

    print("[index_policies] index ready")
    return 0


if __name__ == "__main__":
    sys.exit(main())
