"""FastAPI chat endpoint with function tools (blocking + streaming)."""
import json
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse

from .tools import DISPATCH, TOOL_SCHEMAS

load_dotenv()

app = FastAPI(title="AI-103 chat + tools starter")

_project = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
_deployment = os.environ["MODEL_DEPLOYMENT"]


def _run_tools(tool_calls: list) -> list[dict]:
    """Execute each tool call and return the function_call_output items."""
    outputs: list[dict] = []
    for call in tool_calls:
        func = DISPATCH[call.name]
        result = func(**json.loads(call.arguments))
        outputs.append({
            "type": "function_call_output",
            "call_id": call.call_id,
            "output": json.dumps(result),
        })
    return outputs


@app.post("/chat")
def chat(message: str = Form(...)) -> dict:
    # TODO 1: Open client = _project.get_openai_client().
    # TODO 2: First call client.responses.create(model=_deployment, input=message, tools=TOOL_SCHEMAS).
    # TODO 3: If response.output contains function_call items, call _run_tools(...) and append
    #         outputs via client.responses.create(... previous_response_id=response.id,
    #         input=outputs) until no more tool calls.
    # TODO 4: Return {"reply": final.output_text, "tool_calls": [calls you made]}.
    raise NotImplementedError


@app.post("/stream")
def stream(message: str = Form(...)) -> StreamingResponse:
    # TODO 5: Use client.responses.create(..., stream=True) and yield each event as SSE
    #         lines ("data: <json>\n\n"). Handle response.output_text.delta events for text.
    raise NotImplementedError
