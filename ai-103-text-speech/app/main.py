"""FastAPI for text + speech endpoints."""
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse

from . import speech, text, translate

app = FastAPI(title="AI-103 text + speech starter")


@app.post("/analyze")
def analyze(content: str = Form(...)) -> dict:
    return text.analyze(content)


@app.post("/extract")
def extract(content: str = Form(...)) -> dict:
    return text.extract(content)


@app.post("/translate")
def translate_text(content: str = Form(...), to: str = Form("es")) -> dict:
    return {"text": translate.translate(content, to)}


@app.post("/speak")
def speak(content: str = Form(...)) -> FileResponse:
    out = Path(NamedTemporaryFile(suffix=".wav", delete=False).name)
    speech.synthesize(content, out)
    return FileResponse(out, media_type="audio/wav", filename="speech.wav")


@app.post("/transcribe")
def transcribe(audio: UploadFile = File(...)) -> dict:
    tmp = Path(NamedTemporaryFile(suffix=".wav", delete=False).name)
    tmp.write_bytes(audio.file.read())
    return {"text": speech.transcribe(tmp)}


@app.post("/translate-speech")
def translate_speech(audio: UploadFile = File(...), to: str = Form("es")) -> dict:
    tmp = Path(NamedTemporaryFile(suffix=".wav", delete=False).name)
    tmp.write_bytes(audio.file.read())
    return speech.translate_speech(tmp, to)
