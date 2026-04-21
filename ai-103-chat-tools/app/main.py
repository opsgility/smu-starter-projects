"""Summitline Outfitters chat API.

FastAPI app exposing two endpoints that sit in front of the OpenAI
**Responses API** via Azure AI Foundry:

* ``POST /chat``        — non-streaming; runs a tool-call loop until the
  model emits a final text answer (Exercise 1, TODOs 1-4).
* ``POST /chat/stream`` — streams ``response.output_text.delta`` events
  back to the client as Server-Sent Events (Exercise 2, TODO 5).

The ``AIProjectClient.get_openai_client()`` context manager gives us a
pre-configured OpenAI client that:

* authenticates keylessly using ``DefaultAzureCredential`` (so local
  ``az login`` works and so does production managed identity),
* routes through the Foundry project's content-safety filter, and
* targets the correct regional Responses endpoint for the project.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Iterable, List

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse

from app.tools import DISPATCH, TOOL_SCHEMAS


# ---------------------------------------------------------------------------
# Configuration + clients
# ---------------------------------------------------------------------------

load_dotenv()

_PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
_deployment = os.environ["MODEL_DEPLOYMENT"]

# One long-lived credential + project client for the whole app. The
# OpenAI client itself is created per-request via
# ``_project.get_openai_client()`` so its HTTP session is cleanly scoped
# to the request.
_credential = DefaultAzureCredential()
_project = AIProjectClient(endpoint=_PROJECT_ENDPOINT, credential=_credential)


app = FastAPI(
    title="Summitline Outfitters Chat API",
    description=(
        "FastAPI front-end over the OpenAI Responses API via Azure AI "
        "Foundry. Supports function tools and SSE streaming."
    ),
    version="0.1.0",
)


# ---------------------------------------------------------------------------
# Helper: dispatch one round of function_call items
# ---------------------------------------------------------------------------

def _run_tools(tool_calls: Iterable[Any]) -> List[Dict[str, Any]]:
    """Execute each ``function_call`` and return ``function_call_output`` items.

    The Responses API expects tool results as a list of entries shaped
    like::

        {"type": "function_call_output",
         "call_id": <the call_id from the incoming function_call>,
         "output": <JSON string of the tool's return value>}

    ``call_id`` must echo the incoming call's ``call_id`` verbatim, and
    ``output`` MUST be a string (wrap dicts/lists with ``json.dumps``).
    """
    outputs: List[Dict[str, Any]] = []
    for call in tool_calls:
        fn = DISPATCH.get(call.name)
        if fn is None:
            result: Any = {"error": f"unknown tool: {call.name}"}
        else:
            # `arguments` is a JSON **string** on the wire — parse it first.
            try:
                kwargs = json.loads(call.arguments) if call.arguments else {}
            except json.JSONDecodeError as exc:
                result = {"error": f"invalid JSON arguments: {exc}"}
            else:
                try:
                    result = fn(**kwargs)
                except TypeError as exc:
                    result = {"error": f"bad arguments to {call.name}: {exc}"}
                except Exception as exc:  # pragma: no cover - defensive
                    result = {"error": f"{call.name} failed: {exc}"}

        outputs.append(
            {
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": json.dumps(result),
            }
        )
    return outputs


# ---------------------------------------------------------------------------
# POST /chat  (Exercise 1 — TODOs 1-4)
# ---------------------------------------------------------------------------

@app.post("/chat")
def chat(message: str = Form(...)) -> dict:
    """Handle one user message; loop until the model stops calling tools.

    Pattern:
      1. First ``responses.create`` with the user message + TOOL_SCHEMAS.
      2. Inspect ``response.output``; filter ``function_call`` items.
      3. If none, return ``response.output_text`` — we're done.
      4. Otherwise execute the tools via ``_run_tools`` and call
         ``responses.create`` again with the outputs AND
         ``previous_response_id=response.id`` so the server threads state.
    """
    calls_made: list[dict] = []

    with _project.get_openai_client() as client:
        # TODO (Exercise 1 Step 8 — TODO 1): Make the initial responses.create call.
        #   Pass model=_deployment, input=message, tools=TOOL_SCHEMAS.
        #   Assign the result to a variable named `response`.
        response = None  # replace me

        while True:
            # TODO (Exercise 1 Step 8 — TODO 2): From response.output, collect
            #   every item whose .type == "function_call" into `tool_calls`.
            #   If the list is empty, break out of the loop — the model is done.
            tool_calls: list = []  # replace me

            if not tool_calls:
                break

            for call in tool_calls:
                calls_made.append({"name": call.name, "arguments": call.arguments})

            # TODO (Exercise 1 Step 8 — TODO 3): Run the tools via _run_tools(tool_calls).
            #   Store the returned list in a variable named `outputs`.
            outputs: list = []  # replace me

            # TODO (Exercise 1 Step 8 — TODO 4): Call responses.create again with
            #   input=outputs, previous_response_id=response.id, tools=TOOL_SCHEMAS,
            #   and re-assign the result to `response` so the loop re-checks
            #   for more function calls.
            response = response  # replace me

    return {"reply": response.output_text, "tool_calls": calls_made}


# ---------------------------------------------------------------------------
# POST /chat/stream  (Exercise 2 — TODO 5)
# ---------------------------------------------------------------------------

@app.post("/chat/stream")
def stream(message: str = Form(...)) -> StreamingResponse:
    """Stream the model's reply token-by-token as Server-Sent Events.

    Each ``response.output_text.delta`` event becomes one SSE frame:

        data: {"delta": "..."}\\n\\n

    When ``response.completed`` fires, emit a final ``data: [DONE]\\n\\n``
    sentinel so the client knows to close the connection.
    """

    def event_gen():
        # TODO (Exercise 2 Step 1 — TODO 5): Inside `with _project.get_openai_client() as client:`
        #   call client.responses.create(model=_deployment, input=message,
        #   tools=TOOL_SCHEMAS, stream=True) as a context manager. Iterate the
        #   events; when event.type == "response.output_text.delta",
        #   yield f"data: {json.dumps({'delta': event.delta})}\n\n". When
        #   event.type == "response.completed", yield "data: [DONE]\n\n" and
        #   return.
        raise NotImplementedError("Implement TODO 5 in Exercise 2.")

    return StreamingResponse(event_gen(), media_type="text/event-stream")


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/healthz")
def healthz() -> dict:
    """Liveness probe that does not touch Azure — handy during scaffolding."""
    return {"status": "ok", "deployment": _deployment}
