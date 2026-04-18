"""FastAPI front-end for all four vision endpoints."""
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import Response

from . import caption as cap
from . import edit as ed
from . import generate as gen
from . import inject_detect as inj

app = FastAPI(title="AI-103 vision starter")


@app.post("/generate")
def generate(prompt: str = Form(...)) -> Response:
    return Response(gen.generate(prompt), media_type="image/png")


@app.post("/edit")
def edit(image: UploadFile = File(...), mask: UploadFile = File(...), prompt: str = Form(...)) -> Response:
    return Response(ed.edit(image.file.read(), mask.file.read(), prompt), media_type="image/png")


@app.post("/caption")
def caption(image: UploadFile = File(...), accessibility: bool = Form(False)) -> dict:
    return {"caption": cap.caption(image.file.read(), accessibility=accessibility)}


@app.post("/ask")
def ask(image: UploadFile = File(...), question: str = Form(...)) -> dict:
    return {"answer": cap.answer(image.file.read(), question)}


@app.post("/inject-detect")
def inject_detect(image: UploadFile = File(...)) -> dict:
    return inj.analyze(image.file.read())
