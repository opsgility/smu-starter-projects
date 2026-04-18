"""Orchestrate: blob list → CU extract → embed → upload."""
import json
import os
from typing import Iterable

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import ContainerClient
from dotenv import load_dotenv

from . import cu_extract, index

load_dotenv()

ACCOUNT = os.environ["AZURE_STORAGE_ACCOUNT"]
CONTAINER = os.environ["AZURE_STORAGE_CONTAINER"]
PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
EMBEDDING_DEPLOYMENT = os.environ["EMBEDDING_DEPLOYMENT"]


def _embed(texts: list[str]) -> list[list[float]]:
    with AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential()) as project:
        with project.get_openai_client() as client:
            return [d.embedding for d in client.embeddings.create(model=EMBEDDING_DEPLOYMENT, input=texts).data]


def _chunk(markdown: str, size: int = 1000) -> Iterable[str]:
    for i in range(0, len(markdown), size):
        yield markdown[i:i + size]


def main() -> None:
    cu_extract.ensure_analyzer()
    index.ensure_index()

    # TODO 1: Build a ContainerClient using the storage account URL +
    #         DefaultAzureCredential(). Iterate over container.list_blobs().
    # TODO 2: For each blob: download bytes, call cu_extract.extract(bytes),
    #         chunk the returned markdown.
    # TODO 3: Embed all chunks for that blob in one call to _embed().
    # TODO 4: Build documents [{"id": f"{blob.name}-{i}",
    #                            "source": blob.name,
    #                            "doc_type": fields.get("doc_type",""),
    #                            "markdown": chunk,
    #                            "fields_json": json.dumps(fields),
    #                            "embedding": vec}].
    # TODO 5: index.upload(documents) per blob.
    raise NotImplementedError


if __name__ == "__main__":
    main()
