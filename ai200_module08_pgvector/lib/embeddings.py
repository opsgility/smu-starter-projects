"""Azure OpenAI embeddings — same shape as Module 7."""
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
    r = get_openai().embeddings.create(model=deployment, input=text)
    return r.data[0].embedding
