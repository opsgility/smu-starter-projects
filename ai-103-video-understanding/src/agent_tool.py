"""Foundry Agents FunctionTool wrapper around the Summitline video-segment index.

Implemented in Exercise 6 (TODOs 1-3).

The agent will be able to call `search_video_segments(query)` and receive a
formatted citation string like:

    [Video hero_shot.mp4 @ 00:01:23-00:02:10] Presenter pitches the 3-season
    tent in gusty conditions...

Foundry Agents expects tool returns to serialize cleanly into the message
stream, so we return a single string field (NOT a nested dict) - flat strings
are what the model can quote back into its reply.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Set

from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from openai import AzureOpenAI


load_dotenv()

SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"]
INDEX_NAME = os.environ["AZURE_SEARCH_INDEX_NAME"]
EMBEDDING_DEPLOYMENT = os.environ["EMBEDDING_DEPLOYMENT"]


def _search_client() -> SearchClient:
    return SearchClient(endpoint=SEARCH_ENDPOINT, index_name=INDEX_NAME,
                        credential=DefaultAzureCredential())


def _openai_client() -> AzureOpenAI:
    project = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
    base = project.split("/api/projects/")[0]
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )
    return AzureOpenAI(api_version="2024-10-21", azure_endpoint=base,
                       azure_ad_token_provider=token_provider)


def _format_timestamp(ms: int) -> str:
    """Turn 83000 into 00:01:23."""
    total = int(ms // 1000)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def _embed_query(text: str) -> List[float]:
    client = _openai_client()
    # Exercise 6 - TODO 1
    raise NotImplementedError(
        "Exercise 6 TODO 1: call client.embeddings.create(model=EMBEDDING_DEPLOYMENT, input=text) "
        "and return response.data[0].embedding."
    )


def search_video_segments(query: str, top: int = 3) -> Dict[str, Any]:
    """Search indexed Summitline video segments and return timestamped citations.

    Used by a Foundry agent to answer natural-language questions about product
    videos - the returned `citations` field is a plain string the agent can
    quote back into its reply.

    :param query: Natural-language question about video content (for example,
                  ``"show me videos where the tent is set up in windy conditions"``).
    :param top:   Maximum number of matching segments to return. Default 3.
    :return: A dict with two fields:
             ``citations`` (str) - newline-separated formatted timestamped
             citations, ready to include verbatim in the assistant reply, and
             ``count`` (int) - how many segments matched.
    """
    # Exercise 6 - TODO 2 (embed the query, run vector_queries=[VectorizedQuery(...)])
    # Exercise 6 - TODO 3 (format each hit as "[Video {video_id} @ HH:MM:SS-HH:MM:SS] {scene_summary}"
    #                     joined by "\n", and return the {"citations": ..., "count": ...} dict.)
    raise NotImplementedError(
        "Exercise 6 TODOs 2/3: embed the query via _embed_query(query); run "
        "search_client.search(search_text=None, vector_queries=[VectorizedQuery(vector=q_emb, "
        "k_nearest_neighbors=top, fields='embedding')], select=['video_id','start_ms','end_ms',"
        "'scene_summary']); format each hit as f'[Video {video_id} @ {start}-{end}] {scene_summary}'; "
        "join with '\\n'; return {'citations': ..., 'count': len(hits)}."
    )


# The set of callables FunctionTool converts into tool definitions.
# Keep the name `search_video_segments` - agent instructions reference it.
USER_FUNCTIONS: Set[Any] = {search_video_segments}
