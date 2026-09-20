"""Northwind Horizon capstone — FastAPI app. All routes stubbed."""
from __future__ import annotations

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

app = FastAPI(title="Northwind Horizon Multimodal Assistant")


class ChatIn(BaseModel):
    message: str


@app.post("/chat")
def chat(body: ChatIn) -> dict:
    # TODO (capstone): call foundry.chat_client().complete() with a system + user message.
    return {"error": "not implemented", "hint": "wire foundry.chat_client() from ai-901-chat-client exercise."}


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)) -> dict:
    # TODO (capstone): save upload to temp wav, run Azure Speech SpeechRecognizer, return transcript.
    return {"error": "not implemented", "hint": "reuse the STT code from ai-901-speech."}


@app.post("/vision")
async def vision(file: UploadFile = File(...), question: str = "What's in this image?") -> dict:
    # TODO (capstone): base64-encode upload, send as image_url to a multimodal chat model, return answer.
    return {"error": "not implemented", "hint": "reuse the multimodal chat code from ai-901-vision."}


@app.post("/extract")
async def extract(file: UploadFile = File(...)) -> dict:
    # TODO (capstone): POST to Content Understanding analyzer, poll, return the fields JSON.
    return {"error": "not implemented", "hint": "reuse the poller from ai-901-content-understanding."}


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}
