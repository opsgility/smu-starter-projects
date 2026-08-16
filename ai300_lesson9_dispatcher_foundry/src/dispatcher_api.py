"""
Meridian Dispatcher API — Lesson 9.

FastAPI service that classifies an incoming customer message into exactly one
downstream queue using the versioned prompt at ``prompts/dispatcher_v1.md``
and an ``AIProjectClient`` against the pre-provisioned Azure AI Foundry
``dispatcher`` project.

Run locally:
    uvicorn src.dispatcher_api:app --reload --port 8000
"""

from __future__ import annotations

import json
import logging
import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseModel, Field

load_dotenv()

# --------------------------------------------------------------------------- #
# OpenTelemetry — wire to App Insights if the connection string is present.   #
# --------------------------------------------------------------------------- #
_APP_INSIGHTS_CS = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
if _APP_INSIGHTS_CS:
    configure_azure_monitor(
        connection_string=_APP_INSIGHTS_CS,
        logger_name="dispatcher",
    )

logger = logging.getLogger("dispatcher")
logger.setLevel(logging.INFO)
tracer = trace.get_tracer("dispatcher-api")

# --------------------------------------------------------------------------- #
# Config                                                                      #
# --------------------------------------------------------------------------- #
FOUNDRY_ENDPOINT = os.environ.get("AZURE_FOUNDRY_ENDPOINT", "").rstrip("/")
FOUNDRY_PROJECT = os.environ.get("AZURE_FOUNDRY_PROJECT", "dispatcher")
CHAT_DEPLOYMENT = os.environ.get("CHAT_DEPLOYMENT", "gpt-5.1")

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"
ACTIVE_PROMPT_FILE = os.environ.get("ACTIVE_PROMPT", "dispatcher_v1.md")

VALID_QUEUES = {"CLAIMS", "BILLING", "POLICY_CHANGES", "ROADSIDE", "ESCALATION"}


# --------------------------------------------------------------------------- #
# Prompt loading — front-matter + body                                        #
# --------------------------------------------------------------------------- #
_FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def _parse_front_matter(text: str) -> tuple[dict[str, Any], str]:
    """Split a Markdown file into (front-matter dict, body string).

    We deliberately avoid a YAML dependency — the lab prompts use flat
    ``key: value`` pairs plus a single ``purpose: >`` folded scalar.
    """
    match = _FRONT_MATTER_RE.match(text)
    if not match:
        return {}, text.strip()

    fm_text, body = match.group(1), match.group(2)
    meta: dict[str, Any] = {}
    current_key: str | None = None
    for line in fm_text.splitlines():
        if not line.strip():
            continue
        if line.startswith(" ") and current_key is not None:
            meta[current_key] = f"{meta[current_key]} {line.strip()}".strip()
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value in {">", "|"}:
                meta[key] = ""
                current_key = key
            else:
                meta[key] = value
                current_key = key
    return meta, body.strip()


@lru_cache(maxsize=8)
def load_prompt(name: str) -> tuple[dict[str, Any], str]:
    path = PROMPTS_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"prompt {name!r} not found under {PROMPTS_DIR}")
    return _parse_front_matter(path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Foundry client                                                              #
# --------------------------------------------------------------------------- #
@lru_cache(maxsize=1)
def _project_client() -> AIProjectClient:
    if not FOUNDRY_ENDPOINT:
        raise RuntimeError("AZURE_FOUNDRY_ENDPOINT is not set")
    return AIProjectClient(
        endpoint=f"{FOUNDRY_ENDPOINT}/api/projects/{FOUNDRY_PROJECT}",
        credential=DefaultAzureCredential(),
    )


# --------------------------------------------------------------------------- #
# FastAPI                                                                     #
# --------------------------------------------------------------------------- #
app = FastAPI(
    title="Meridian Dispatcher",
    version="0.1.0",
    description=(
        "Routes an incoming Meridian Insurance customer message to exactly "
        "one downstream queue using the versioned prompt at "
        "prompts/dispatcher_v1.md."
    ),
)
FastAPIInstrumentor.instrument_app(app)


class DispatchRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=8000)
    prompt_version: str | None = Field(
        default=None,
        description="Optional override, e.g. 'dispatcher_v2.md'.",
    )


class DispatchResponse(BaseModel):
    queue: str
    confidence: float
    reason: str
    prompt_version: str
    model: str


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/dispatch", response_model=DispatchResponse)
def dispatch(req: DispatchRequest) -> DispatchResponse:
    prompt_file = req.prompt_version or ACTIVE_PROMPT_FILE
    with tracer.start_as_current_span("dispatcher.classify") as span:
        span.set_attribute("dispatcher.prompt_version", prompt_file)
        span.set_attribute("dispatcher.model", CHAT_DEPLOYMENT)

        meta, body = load_prompt(prompt_file)
        temperature = float(meta.get("temperature", "0.2"))

        client = _project_client()
        chat = client.inference.get_chat_completions_client()
        completion = chat.complete(
            model=CHAT_DEPLOYMENT,
            messages=[
                {"role": "system", "content": body},
                {"role": "user", "content": req.message},
            ],
            temperature=temperature,
            response_format={"type": "json_object"},
        )
        raw = completion.choices[0].message.content or "{}"

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as err:
            logger.exception("dispatcher returned non-JSON: %s", raw)
            raise HTTPException(status_code=502, detail="model returned non-JSON") from err

        queue = str(payload.get("queue", "")).strip().upper()
        if queue not in VALID_QUEUES:
            span.set_attribute("dispatcher.invalid_queue", queue or "<empty>")
            queue = "ESCALATION"
            payload["reason"] = "invalid_queue_fallback"

        span.set_attribute("dispatcher.queue", queue)

        return DispatchResponse(
            queue=queue,
            confidence=float(payload.get("confidence", 0.0)),
            reason=str(payload.get("reason", ""))[:200],
            prompt_version=prompt_file,
            model=CHAT_DEPLOYMENT,
        )
