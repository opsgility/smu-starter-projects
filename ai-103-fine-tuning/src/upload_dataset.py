"""Upload the Summitline gear-recommendation JSONL as a fine-tuning training file.

Exercise 3 Steps 3-5.

Reads   data/gear_recommendations.jsonl
Writes  data/uploaded_file_id.txt   (the fine-tuning file ID, e.g. file-abc...)

The Azure OpenAI fine-tuning file endpoint accepts JSONL files uploaded via the
`files` API with purpose=`fine-tune`. The file must be UTF-8 encoded with a
byte-order mark (BOM) per MS Learn:
https://learn.microsoft.com/azure/foundry/openai/how-to/fine-tuning#prepare-your-training-and-validation-data

Run:
    python src/upload_dataset.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AzureOpenAI


REPO_ROOT = Path(__file__).resolve().parent.parent
TRAINING_JSONL = REPO_ROOT / "data" / "gear_recommendations.jsonl"
UPLOADED_FILE_ID = REPO_ROOT / "data" / "uploaded_file_id.txt"


def build_client() -> AzureOpenAI:
    """Construct a keyless AzureOpenAI client backed by DefaultAzureCredential."""
    load_dotenv()
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )
    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_ad_token_provider=token_provider,
        api_version="2024-10-21",
    )


def upload_training_file() -> str:
    """Upload the JSONL as a fine-tuning file and return the file ID.

    TODO (Exercise 3 Step 3):
        Read TRAINING_JSONL as binary bytes.
        Prepend a UTF-8 BOM (b'\\xef\\xbb\\xbf') if it isn't already present —
        Azure OpenAI's fine-tuning file validator requires it.
        Call `client.files.create(file=..., purpose="fine-tune")` and return
        the resulting `.id`.
    """
    _client = build_client()  # noqa: F841 — used by your implementation
    # ---- Exercise 3 Step 3 Start ----
    raise NotImplementedError("Implement upload_training_file — Exercise 3 Step 3")
    # ---- Exercise 3 Step 3 End ----


def main() -> int:
    if not TRAINING_JSONL.exists():
        print(f"ERROR: {TRAINING_JSONL} not found.", file=sys.stderr)
        return 1
    file_id = upload_training_file()
    UPLOADED_FILE_ID.write_text(file_id, encoding="utf-8")
    print(f"Uploaded fine-tuning file: {file_id}")
    print(f"Saved to: {UPLOADED_FILE_ID}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
