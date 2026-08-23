"""Drive a Foundry agent end-to-end against the video-segment index.

Implemented in Exercise 7 (TODOs 1-3). Sends the "windy tent" query through
a fresh agent whose only tool is `search_video_segments` from
`src/agent_tool.py`. The agent decides whether to call the tool, gets back
timestamped citations, and quotes them into its reply.

Expected transcript when everything is wired:

    USER      | show me videos where the tent is set up in windy conditions
    ASSISTANT | I found two segments...
                [Video hero_shot.mp4 @ 00:01:23-00:02:10] Presenter pitches...
                [Video field_test.mp4 @ 00:00:45-00:01:20] Tent stakes hold...

Run with:
    python src/end_to_end_query.py
"""
from __future__ import annotations

import os
import sys
from typing import List, Dict

from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FunctionTool, ToolSet, ListSortOrder

from src.agent_tool import USER_FUNCTIONS


load_dotenv()

PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
MODEL = os.environ["MODEL_DEPLOYMENT"]
QUERY = "show me videos where the tent is set up in windy conditions"

AGENT_INSTRUCTIONS = (
    "You are the Summitline Outfitters video search assistant. When the user "
    "asks about product-demo video content, ALWAYS call the "
    "search_video_segments tool - never guess from memory. When the tool "
    "returns citations, quote each citation verbatim (do not paraphrase the "
    "'[Video ... @ ...]' prefix - it is the timestamp anchor). If the tool "
    "returns count=0, say you did not find matching segments. Keep replies "
    "concise: one sentence of context, then the citations."
)


def build_client() -> AgentsClient:
    """Foundry AgentsClient authenticated with DefaultAzureCredential."""
    return AgentsClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())


def run_query(query: str) -> List[Dict[str, str]]:
    """Drive one query through a fresh agent + thread, return the transcript."""
    with build_client() as client:
        # Exercise 7 - TODO 1 (register USER_FUNCTIONS via ToolSet + enable_auto_function_calls,
        #                      then create_agent with model=MODEL, instructions=AGENT_INSTRUCTIONS,
        #                      tools=toolset.definitions, tool_resources=toolset.resources)
        # Exercise 7 - TODO 2 (create thread, post user message, runs.create_and_process,
        #                      assert run.status == "completed")
        # Exercise 7 - TODO 3 (read messages back with ListSortOrder.ASCENDING, format the
        #                      role/text transcript, and call client.delete_agent in a finally
        #                      block so agents don't leak)
        raise NotImplementedError(
            "Exercise 7 TODOs 1/2/3: wire ToolSet -> create_agent -> thread -> "
            "runs.create_and_process -> read transcript -> delete_agent."
        )


def main() -> None:
    transcript = run_query(QUERY)
    for turn in transcript:
        role = turn.get("role", "?").upper()
        text = turn.get("text", "")
        print(f"{role:<9} | {text}")


if __name__ == "__main__":
    try:
        main()
    except NotImplementedError as exc:
        print(f"\n[TODO]     {exc}", file=sys.stderr)
        sys.exit(2)
