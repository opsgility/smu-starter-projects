"""Foundry IQ RAG query surface for investment_researcher.

Retrieves top-k grounded snippets from the Ridgevault research index for a
free-text question. Returns them as a single formatted string ready to be
injected into the model call as a system message.

Exercise 5 uses this from `agents/investment_researcher.py` — you do NOT need
to modify this file. Reading it end-to-end IS part of Exercise 5, because you
must understand how the citation format is wired before you can teach the
system prompt to reference it.
"""
from __future__ import annotations
import os
from typing import List

from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv


def query_index(question: str, top_k: int = 3) -> str:
    """Return top_k grounded snippets from the Ridgevault research index.

    Format returned to the caller (safe to prepend to messages verbatim):

        Ridgevault research context. Cite by title.
        --- [ridgevault-market-brief] ---
        <chunk text>
        --- [ridgevault-sector-outlook] ---
        <chunk text>
    """
    load_dotenv()
    endpoint = os.environ["SEARCH_ENDPOINT"]
    index_name = os.environ["SEARCH_INDEX_NAME"]

    client = SearchClient(
        endpoint=endpoint,
        index_name=index_name,
        credential=DefaultAzureCredential(),
    )
    results = client.search(search_text=question, top=top_k, select=["title", "chunk"])

    lines: List[str] = ["Ridgevault research context. Cite by title."]
    any_hits = False
    for hit in results:
        any_hits = True
        title = hit.get("title", "unknown")
        chunk = hit.get("chunk", "")
        lines.append(f"--- [{title}] ---")
        lines.append(chunk)

    if not any_hits:
        lines.append("(no Ridgevault documents matched — do NOT fabricate a citation)")

    return "\n".join(lines)
