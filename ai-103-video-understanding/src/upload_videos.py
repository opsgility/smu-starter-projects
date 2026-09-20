"""Upload sample Summitline product-demo videos to the `videos` blob container.

Implemented across Exercise 2 (TODOs 1-4). All auth is keyless via
`DefaultAzureCredential`. The storage account was deployed with
`allowSharedKeyAccess: false`, so shared-key SAS is never used - user-delegation
SAS is minted from the caller's Entra token when Content Understanding needs
a URL to fetch (Exercise 4 uses those).

Sample-video sources are named in `sample-videos/README.md`. The starter
downloads them from public URLs at lab time rather than baking large binaries
into the repo.

Run with:
    python src/upload_videos.py
"""
from __future__ import annotations

import os
import pathlib
import sys
from datetime import datetime, timedelta, timezone
from typing import List, Tuple

from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.storage.blob import (
    BlobServiceClient,
    BlobSasPermissions,
    generate_blob_sas,
)


load_dotenv()

STORAGE_ACCOUNT = os.environ["AZURE_STORAGE_ACCOUNT_NAME"]
CONTAINER_NAME = "videos"
LOCAL_SAMPLES_DIR = pathlib.Path(__file__).parent.parent / "sample-videos"


# Small public product-demo MP4s the exercises reference. Keep the filename
# stable - the CU analyzer scenes are described in the exercise text using
# these names, and the agent tool cites them by filename.
SAMPLE_URLS: List[Tuple[str, str]] = [
    # (blob_name, source_url)
    # See sample-videos/README.md for how to fetch these locally if you want
    # to inspect them before uploading.
    ("hero_shot.mp4",
     "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-quickstart-code/master/python/ContentUnderstanding/videos/hero_shot.mp4"),
    ("field_test.mp4",
     "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-quickstart-code/master/python/ContentUnderstanding/videos/field_test.mp4"),
]


def build_service_client() -> BlobServiceClient:
    """AAD-only BlobServiceClient - no shared key, no connection string."""
    # Exercise 2 - TODO 1
    raise NotImplementedError(
        "Exercise 2 TODO 1: construct BlobServiceClient using the account URL "
        f"'https://{STORAGE_ACCOUNT}.blob.core.windows.net' and DefaultAzureCredential()."
    )


def ensure_container(service: BlobServiceClient) -> None:
    """The ARM template pre-creates 'videos', so this is idempotent."""
    # Exercise 2 - TODO 2
    raise NotImplementedError(
        "Exercise 2 TODO 2: get_container_client(CONTAINER_NAME) and call create_container() "
        "inside a try/except ResourceExistsError block."
    )


def download_sample(url: str, dest: pathlib.Path) -> pathlib.Path:
    """Download one small MP4 into sample-videos/ if it isn't already there."""
    # Exercise 2 - TODO 3
    raise NotImplementedError(
        "Exercise 2 TODO 3: use urllib.request.urlretrieve or requests.get with stream=True "
        "to save the URL to `dest`. Skip the download if the file already exists."
    )


def upload_one(service: BlobServiceClient, blob_name: str, local_path: pathlib.Path) -> None:
    """Upload a single MP4, overwriting if it already exists."""
    # Exercise 2 - TODO 4
    raise NotImplementedError(
        "Exercise 2 TODO 4: get_blob_client(container=CONTAINER_NAME, blob=blob_name), "
        "then upload_blob(data=open(local_path,'rb'), overwrite=True, "
        "content_settings=ContentSettings(content_type='video/mp4'))."
    )


def mint_user_delegation_sas(service: BlobServiceClient, blob_name: str,
                             minutes: int = 60) -> str:
    """Mint a read-only user-delegation SAS the CU service can use to fetch a blob.

    Content Understanding's analyze call needs a URL it can GET without any
    caller-supplied auth - user-delegation SAS chains the student's Entra token
    to a time-bounded blob-read SAS.

    Do NOT switch to shared-key SAS - the storage account has
    `allowSharedKeyAccess: false` and the request will 403.
    """
    now = datetime.now(timezone.utc)
    udk = service.get_user_delegation_key(key_start_time=now - timedelta(minutes=2),
                                          key_expiry_time=now + timedelta(minutes=minutes))
    sas = generate_blob_sas(
        account_name=STORAGE_ACCOUNT,
        container_name=CONTAINER_NAME,
        blob_name=blob_name,
        user_delegation_key=udk,
        permission=BlobSasPermissions(read=True),
        expiry=now + timedelta(minutes=minutes),
    )
    return f"https://{STORAGE_ACCOUNT}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}?{sas}"


def main() -> None:
    LOCAL_SAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    service = build_service_client()
    ensure_container(service)

    for blob_name, url in SAMPLE_URLS:
        local = LOCAL_SAMPLES_DIR / blob_name
        download_sample(url, local)
        upload_one(service, blob_name, local)
        print(f"[uploaded] {blob_name} ({local.stat().st_size / 1024:.1f} KB)")

    # Print one signed URL so you can eyeball it - Exercise 4 mints these on demand.
    sample_sas = mint_user_delegation_sas(service, SAMPLE_URLS[0][0], minutes=10)
    print(f"\n[sas]      {SAMPLE_URLS[0][0]} -> {sample_sas[:120]}...")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as exc:
        print(f"\n[TODO]     {exc}", file=sys.stderr)
        sys.exit(2)
