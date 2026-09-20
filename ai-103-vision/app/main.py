"""FastAPI entrypoint for the Summitline Outfitters vision service.

Wires the six endpoints the four Lesson 11 exercises exercise:
  POST /generate        -> images.generate (Exercise 1)
  POST /edit            -> images.edit inpainting (Exercise 1)
  POST /caption         -> Responses API caption / alt-text (Exercise 2)
  POST /ask             -> Responses API visual Q&A (Exercise 2)
  POST /visual-analyze  -> Content Understanding analyzer (Exercise 3)
  POST /inject-detect   -> indirect prompt-injection detector (Exercise 4)
"""
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import Response

from . import caption as caption_mod
from . import cu_visual
from . import edit as edit_mod
from . import generate as generate_mod
from . import inject_detect

app = FastAPI(title="Summitline Outfitters Vision", version="1.0.0")


@app.get("/")
def root() -> dict:
    return {
        "service": "Summitline Outfitters Vision",
        "endpoints": [
            "/generate",
            "/edit",
            "/caption",
            "/ask",
            "/visual-analyze",
            "/inject-detect",
        ],
    }


@app.post("/generate")
def generate_endpoint(
    prompt: str = Form(...),
    size: str = Form("1024x1024"),
) -> Response:
    """Exercise 1 — text-to-image. Returns the raw PNG bytes."""
    png = generate_mod.generate(prompt, size=size)
    return Response(content=png, media_type="image/png")


@app.post("/edit")
def edit_endpoint(
    image: UploadFile = File(...),
    mask: UploadFile = File(...),
    prompt: str = Form(...),
) -> Response:
    """Exercise 1 — inpaint masked region. Returns the edited PNG bytes."""
    png = edit_mod.edit(image.file.read(), mask.file.read(), prompt)
    return Response(content=png, media_type="image/png")


@app.post("/caption")
def caption_endpoint(
    image: UploadFile = File(...),
    accessibility: bool = Form(False),
) -> dict:
    """Exercise 2 — caption or accessibility alt-text."""
    text = caption_mod.caption(image.file.read(), accessibility=accessibility)
    return {"caption": text}


@app.post("/ask")
def ask_endpoint(
    image: UploadFile = File(...),
    question: str = Form(...),
) -> dict:
    """Exercise 2 — visual Q&A."""
    text = caption_mod.answer(image.file.read(), question)
    return {"answer": text}


@app.post("/visual-analyze")
def visual_analyze_endpoint(image: UploadFile = File(...)) -> dict:
    """Exercise 3 — Content Understanding structured extraction."""
    return cu_visual.analyze(image.file.read())


@app.post("/inject-detect")
def inject_detect_endpoint(image: UploadFile = File(...)) -> dict:
    """Exercise 4 — indirect prompt-injection detector."""
    return inject_detect.analyze(image.file.read())
