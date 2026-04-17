"""
FastAPI entrypoint for the AI-901 capstone assistant.
Each route delegates to a module that you complete in the exercise.
"""
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from app import chat, documents, speech, text, vision

app = FastAPI(title="Northwind Horizon AI Assistant")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/chat")
def chat_endpoint(message: str = Form(...)) -> JSONResponse:
    # TODO 1: call chat.reply(message) and return {"reply": ...} as JSON.
    raise NotImplementedError


@app.post("/analyze-text")
def text_endpoint(content: str = Form(...)) -> JSONResponse:
    # TODO 2: call text.analyze(content) and return the result.
    raise NotImplementedError


@app.post("/analyze-image")
async def vision_endpoint(file: UploadFile = File(...), question: str = Form(...)) -> JSONResponse:
    # TODO 3: save the upload to a temp path, pass it to vision.analyze(path, question), return the result.
    raise NotImplementedError


@app.post("/extract-document")
async def document_endpoint(file: UploadFile = File(...)) -> JSONResponse:
    # TODO 4: save the upload, call documents.extract(path), return extracted fields.
    raise NotImplementedError


@app.post("/speak")
def speak_endpoint(content: str = Form(...)) -> FileResponse:
    # TODO 5: call speech.synthesize(content, out_path=Path("reply.wav")), return FileResponse("reply.wav").
    raise NotImplementedError
