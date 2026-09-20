"""Azure OpenAI embeddings wrapper. Reads endpoint + key + deployment from env."""
from __future__ import annotations

import os
from functools import lru_cache

from openai import AzureOpenAI


@lru_cache(maxsize=1)
def get_openai() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_KEY"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    )


def embed(text: str) -> list[float]:
    deployment = os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"]
    result = get_openai().embeddings.create(model=deployment, input=text)
    return result.data[0].embedding


def embed_batch(texts: list[str]) -> list[list[float]]:
    deployment = os.environ["AZURE_OPENAI_EMBED_DEPLOYMENT"]
    result = get_openai().embeddings.create(model=deployment, input=texts)
    return [d.embedding for d in result.data]
