"""Azure OpenAI embeddings + chat — pre-written."""
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


def chat(prompt: str, context: list[str]) -> str:
    deployment = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]
    context_block = "\n\n".join(f"- {c}" for c in context)
    r = get_openai().chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system",
             "content": "You are a Northwind Logistics support agent. Answer using ONLY the context. "
                        "If the context doesn't cover the question, say so plainly."},
            {"role": "user", "content": f"Question: {prompt}\n\nContext:\n{context_block}"},
        ],
        temperature=0.2,
        max_tokens=300,
    )
    return r.choices[0].message.content or ""
