# AI-103 Lesson 11 — Computer Vision Starter

Scaffold for image generation, image editing (inpainting), multimodal understanding (caption +
visual Q&A), and indirect-prompt-injection detection from images.

## Files

- `app/generate.py`      — text-to-image with `gpt-image-1` (Foundry deployment)
- `app/edit.py`          — image editing (inpainting via mask)
- `app/caption.py`       — captions + visual Q&A using a multimodal chat model
- `app/inject_detect.py` — read text from an image and decide whether it's a prompt-injection attempt
- `app/main.py`          — FastAPI exposing all four

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
az login
uvicorn app.main:app --reload --port 8000
```
