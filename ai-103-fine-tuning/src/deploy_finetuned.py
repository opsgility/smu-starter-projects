"""Deploy the fine-tuned Summitline concierge model on a Developer-SKU deployment.

Exercise 6 Steps 2-4.

Reads   data/finetuned_model_name.txt      (produced by Exercise 5)
Writes  data/finetuned_deployment_name.txt (the new deployment name)

Deployment tier: `Developer` — pay-per-token only, no hourly hosting fee, no SLA,
24-hour lifetime. Perfect for evaluating a fine-tuned model before promoting.
Reference: https://learn.microsoft.com/azure/ai-foundry/openai/how-to/fine-tune-test
(verified 2026-08-23).

This deploy is an ARM operation on `Microsoft.CognitiveServices/accounts/deployments`
which requires Owner on the parent scope. The lab pre-creates a resource group
so the platform grants the student Owner at that RG scope — no elevation on the
subscription-scope credential is needed. Uses the `azure-mgmt-cognitiveservices`
SDK (already preinstalled in the python-ai container).

Run:
    python src/deploy_finetuned.py
"""
from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient


REPO_ROOT = Path(__file__).resolve().parent.parent
FINETUNED_MODEL_NAME = REPO_ROOT / "data" / "finetuned_model_name.txt"
FINETUNED_DEPLOYMENT_NAME = REPO_ROOT / "data" / "finetuned_deployment_name.txt"

DEPLOYMENT_SKU = "Developer"
DEPLOYMENT_SKU_CAPACITY = 50  # Per MS Learn Developer-SKU example.


def _resolve_context() -> dict:
    """Look up the current subscription, resource group, and Foundry account name.

    The starter's .env carries AZURE_OPENAI_ENDPOINT; we derive the account
    name from its hostname. Subscription + RG are picked up from `az account`
    context and `az group list`.
    """
    load_dotenv()
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    # Endpoint shape: https://<account>.openai.azure.com
    match = re.match(r"^https?://([^.]+)\.", endpoint)
    if not match:
        raise RuntimeError(f"Could not parse Foundry account name from {endpoint!r}.")
    account_name = match.group(1)

    from azure.cli.core import get_default_cli  # part of the azure-cli package preinstalled in the container

    cli = get_default_cli()
    cli.invoke(["account", "show", "--query", "id", "-o", "tsv"], out_file=open(os.devnull, "w"))
    subscription_id = cli.result.result
    if not subscription_id:
        raise RuntimeError("`az account show` returned no subscription. Run `az login --use-device-code`.")

    cli.invoke(
        [
            "group",
            "list",
            "--query",
            "[?starts_with(name, 'summitline-finetune')].name | [0]",
            "-o",
            "tsv",
        ],
        out_file=open(os.devnull, "w"),
    )
    resource_group = cli.result.result
    if not resource_group:
        raise RuntimeError("No resource group starting with 'summitline-finetune' found.")

    return {
        "subscription_id": subscription_id,
        "resource_group": resource_group,
        "account_name": account_name,
    }


def deploy_finetuned_model(fine_tuned_model: str) -> str:
    """Create a Developer-SKU deployment for `fine_tuned_model` and return the deployment name.

    TODO (Exercise 6 Step 3):
        Build a unique deployment name: f"summitline-concierge-ft-{int(time.time())}".
        Use CognitiveServicesManagementClient(cred, subscription_id).deployments.begin_create_or_update(
            resource_group_name=ctx["resource_group"],
            account_name=ctx["account_name"],
            deployment_name=deployment_name,
            deployment={
                "sku": {"name": "Developer", "capacity": 50},
                "properties": {
                    "model": {
                        "format": "OpenAI",
                        "name": fine_tuned_model,   # e.g. "ft:gpt-4.1-mini-2025-04-14:..."
                        "version": "1",
                    }
                },
            },
        ).result()
        Return deployment_name.
    """
    _ctx = _resolve_context()  # noqa: F841 — used by your implementation
    _cred = DefaultAzureCredential()  # noqa: F841
    _deployment_name = f"summitline-concierge-ft-{int(time.time())}"  # noqa: F841
    # ---- Exercise 6 Step 3 Start ----
    raise NotImplementedError("Implement deploy_finetuned_model — Exercise 6 Step 3")
    # ---- Exercise 6 Step 3 End ----


def main() -> int:
    if not FINETUNED_MODEL_NAME.exists():
        print(
            f"ERROR: {FINETUNED_MODEL_NAME} not found — run src/poll_job_status.py first.",
            file=sys.stderr,
        )
        return 1
    fine_tuned_model = FINETUNED_MODEL_NAME.read_text(encoding="utf-8").strip()
    deployment_name = deploy_finetuned_model(fine_tuned_model)
    FINETUNED_DEPLOYMENT_NAME.write_text(deployment_name, encoding="utf-8")
    print(f"Deployed fine-tuned model as: {deployment_name}")
    print(f"SKU: {DEPLOYMENT_SKU} (24-hour lifetime, per-token billing).")
    print(f"Saved to: {FINETUNED_DEPLOYMENT_NAME}")
    print("Next: python src/compare_base_vs_finetuned.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
