"""Capstone FastAPI orchestrator."""
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, Response

from . import agent, chat, cu, rag, speech, tracing, vision

app = FastAPI(title="AI-103 capstone — Northwind Horizon")
_tracer = tracing.init()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat")
def chat_ep(message: str = Form(...)) -> dict:
    with _tracer.start_as_current_span("/chat"):
        return {"reply": chat.reply(message)}


@app.post("/rag")
def rag_ep(question: str = Form(...)) -> dict:
    with _tracer.start_as_current_span("/rag"):
        return rag.answer(question)


@app.post("/agent")
def agent_ep(message: str = Form(...)) -> dict:
    with _tracer.start_as_current_span("/agent"):
        return {"reply": agent.run(message)}


@app.post("/vision-ask")
def vision_ep(image: UploadFile = File(...), question: str = Form(...)) -> dict:
    with _tracer.start_as_current_span("/vision-ask"):
        return {"answer": vision.ask(image.file.read(), question)}


@app.post("/extract-doc")
def extract_doc(file: UploadFile = File(...)) -> dict:
    with _tracer.start_as_current_span("/extract-doc"):
        return {"fields": cu.extract(file.file.read())}


@app.post("/voice")
def voice(audio: UploadFile = File(...)) -> FileResponse:
    """STT → chat → TTS, wired end-to-end."""
    with _tracer.start_as_current_span("/voice"):
        in_path = Path(NamedTemporaryFile(suffix=".wav", delete=False).name)
        in_path.write_bytes(audio.file.read())
        text = speech.transcribe(in_path)
        reply_text = chat.reply(text)
        out_path = Path(NamedTemporaryFile(suffix=".wav", delete=False).name)
        speech.synthesize(reply_text, out_path)
        return FileResponse(out_path, media_type="audio/wav", filename="reply.wav")
