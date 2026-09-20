"""Create a fine-tuning job on gpt-4.1-mini using the uploaded Summitline training file.

Exercise 4 Steps 2-4.

Reads   data/uploaded_file_id.txt   (produced by Exercise 3)
Writes  data/finetune_job_id.txt    (the job ID, e.g. ftjob-abc...)

Base model + method (verified 2026-08-23 per MS Learn
https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#fine-tuning-models):

    model  = gpt-4.1-mini-2025-04-14
    method = SFT (Supervised Fine-Tuning)
    tier   = Global (specified via extra_body when api-version=2025-04-01-preview)

Run:
    python src/start_finetune_job.py
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI


REPO_ROOT = Path(__file__).resolve().parent.parent
UPLOADED_FILE_ID = REPO_ROOT / "data" / "uploaded_file_id.txt"
FINETUNE_JOB_ID = REPO_ROOT / "data" / "finetune_job_id.txt"

# Base model — verified GA + SFT-supported on 2026-08-23.
BASE_MODEL = "gpt-4.1-mini-2025-04-14"


def build_client() -> AzureOpenAI:
    load_dotenv()
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )
    # Preview api-version is required to opt in to the Global training tier.
    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
        api_version="2025-04-01-preview",
    )


def start_finetune_job(file_id: str) -> str:
    """Create an SFT fine-tuning job on BASE_MODEL and return the job ID.

    TODO (Exercise 4 Step 3):
        Call `client.fine_tuning.jobs.create(...)` with:
            - training_file = file_id
            - model = BASE_MODEL
            - suffix = os.environ["FINETUNE_JOB_NAME_PREFIX"] + "-" + int(time.time())
            - seed = 42  (so re-runs are reproducible)
            - extra_body = {"trainingType": "Global"}  (Global tier — see MS Learn note)
        Return job.id.
    """
    _client = build_client()  # noqa: F841 — used by your implementation
    _suffix = f"{os.environ['FINETUNE_JOB_NAME_PREFIX']}-{int(time.time())}"  # noqa: F841
    # ---- Exercise 4 Step 3 Start ----
    raise NotImplementedError("Implement start_finetune_job — Exercise 4 Step 3")
    # ---- Exercise 4 Step 3 End ----


def main() -> int:
    if not UPLOADED_FILE_ID.exists():
        print(
            f"ERROR: {UPLOADED_FILE_ID} not found — run src/upload_dataset.py first.",
            file=sys.stderr,
        )
        return 1
    file_id = UPLOADED_FILE_ID.read_text(encoding="utf-8").strip()
    job_id = start_finetune_job(file_id)
    FINETUNE_JOB_ID.write_text(job_id, encoding="utf-8")
    print(f"Started fine-tuning job: {job_id}")
    print(f"Base model: {BASE_MODEL}")
    print(f"Saved to: {FINETUNE_JOB_ID}")
    print("Next: python src/poll_job_status.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
