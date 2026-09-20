"""Summitline Outfitters capstone FastAPI app.

Fully wired — the exercises edit the modules imported below, not this file.
Tracing is configured at import time (before ``app = FastAPI()``) so every
route is auto-instrumented.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

# Load .env early so the SDKs see credentials at import time.
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv is in requirements.txt; safe guard anyway.
    pass

# IMPORTANT: configure Azure Monitor OTel BEFORE FastAPI is instantiated.
from app import tracing  # noqa: E402

try:
    tracing.init()
except Exception:  # pragma: no cover - students see the real error in their terminal.
    # Surfaces a clear error the first time a student runs the app without
    # finishing Exercise 1 Step 6.
    raise

from fastapi import FastAPI, File, Form, UploadFile  # noqa: E402
from fastapi.responses import FileResponse, JSONResponse  # noqa: E402

from app import agent, chat, cu, rag, speech, vision  # noqa: E402

app = FastAPI(
    title="Summitline Outfitters Capstone",
    description=(
        "AI-103 Lesson 14 capstone. Six endpoints on one Foundry project, "
        "observable end-to-end in Application Insights."
    ),
    version="1.0.0",
)


@app.get("/health")
def health() -> dict:
    """Liveness probe. Used by test_client.py first."""
    return {"status": "ok"}


@app.post("/chat")
def chat_endpoint(message: str = Form(...)) -> dict:
    """Stateless product / policy chat."""
    return {"reply": chat.reply(message)}


@app.post("/rag")
def rag_endpoint(question: str = Form(...)) -> dict:
    """Grounded answer with citations from summitline-kb."""
    return rag.answer(question)


@app.post("/agent")
def agent_endpoint(message: str = Form(...)) -> dict:
    """Tool-using concierge (AzureAISearchTool + _ship_status)."""
    return {"reply": agent.run(message)}


@app.post("/vision-ask")
async def vision_endpoint(
    image: UploadFile = File(...),
    question: str = Form(...),
) -> dict:
    """Ask a natural-language question about an uploaded image."""
    data = await image.read()
    return {"answer": vision.ask(data, question)}


@app.post("/extract-doc")
async def extract_endpoint(file: UploadFile = File(...)) -> dict:
    """Extract vendor / doc_type / total from a PDF via Content Understanding."""
    data = await file.read()
    return {"fields": cu.extract(data)}


@app.post("/voice")
async def voice_endpoint(audio: UploadFile = File(...)) -> FileResponse:
    """Audio-in -> chat -> audio-out full roundtrip."""
    with tempfile.TemporaryDirectory() as tmpdir:
        in_path = Path(tmpdir) / "input.wav"
        out_path = Path(tmpdir) / "reply.wav"
        in_path.write_bytes(await audio.read())

        text = speech.transcribe(in_path)
        reply_text = chat.reply(text)
        speech.synthesize(reply_text, out_path)

        # Copy out of the temp dir before it's cleaned up.
        final = Path(tempfile.mkstemp(suffix=".wav")[1])
        final.write_bytes(out_path.read_bytes())
        return FileResponse(
            path=str(final),
            media_type="audio/wav",
            filename="reply.wav",
            headers={"X-Transcribed-Text": text[:200]},
        )


@app.exception_handler(NotImplementedError)
def _not_implemented_handler(_request, exc: NotImplementedError) -> JSONResponse:
    """Friendlier 501 when a student hits an endpoint before finishing TODOs."""
    return JSONResponse(status_code=501, content={"error": str(exc)})
