"""Poll a fine-tuning job until it terminates, printing loss + validation metrics.

Exercise 5 Steps 2-4.

Reads   data/finetune_job_id.txt        (produced by Exercise 4)
Writes  data/finetuned_model_name.txt   (the fine-tuned model ID, e.g. ft:gpt-4.1-mini...)

Terminal states: succeeded, failed, cancelled.
On success the fine-tuning job returns a `fine_tuned_model` property — that
value is what you deploy in Exercise 6.

Run:
    python src/poll_job_status.py
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
FINETUNE_JOB_ID = REPO_ROOT / "data" / "finetune_job_id.txt"
FINETUNED_MODEL_NAME = REPO_ROOT / "data" / "finetuned_model_name.txt"

POLL_INTERVAL_SEC = 30
TERMINAL_STATES = {"succeeded", "failed", "cancelled"}


def build_client() -> AzureOpenAI:
    load_dotenv()
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )
    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
        api_version="2025-04-01-preview",
    )


def poll_until_done(job_id: str) -> dict:
    """Poll `fine_tuning.jobs.retrieve(job_id)` every POLL_INTERVAL_SEC.

    TODO (Exercise 5 Step 3):
        Loop:
            job = client.fine_tuning.jobs.retrieve(job_id)
            print(f"[{job.status}] trained_tokens={job.trained_tokens}")
            if job.status in TERMINAL_STATES: break
            time.sleep(POLL_INTERVAL_SEC)
        Return the terminal job object as a dict via job.model_dump().

    TODO (Exercise 5 Step 4):
        Once the job succeeds, also fetch the last 10 events via
        `client.fine_tuning.jobs.list_events(job_id, limit=10)` and print
        each event's message — that's where the loss + validation lines
        surface for the SFT method.
    """
    _client = build_client()  # noqa: F841 — used by your implementation
    # ---- Exercise 5 Step 3 Start ----
    raise NotImplementedError("Implement poll_until_done — Exercise 5 Step 3")
    # ---- Exercise 5 Step 3 End ----


def main() -> int:
    if not FINETUNE_JOB_ID.exists():
        print(
            f"ERROR: {FINETUNE_JOB_ID} not found — run src/start_finetune_job.py first.",
            file=sys.stderr,
        )
        return 1
    job_id = FINETUNE_JOB_ID.read_text(encoding="utf-8").strip()
    print(f"Polling job {job_id} every {POLL_INTERVAL_SEC}s. Fine-tune usually takes 10-15 min.")
    job = poll_until_done(job_id)
    status = job.get("status")
    if status != "succeeded":
        print(f"Fine-tune ended in state: {status!r} — check events for the error.", file=sys.stderr)
        return 1
    ft_model = job.get("fine_tuned_model")
    if not ft_model:
        print("Job succeeded but fine_tuned_model is missing on the payload.", file=sys.stderr)
        return 1
    FINETUNED_MODEL_NAME.write_text(ft_model, encoding="utf-8")
    print(f"Fine-tuned model: {ft_model}")
    print(f"Saved to: {FINETUNED_MODEL_NAME}")
    print("Next: python src/deploy_finetuned.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
