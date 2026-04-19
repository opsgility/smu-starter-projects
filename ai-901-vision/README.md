# ai-901-vision — image analysis + image generation scaffold

Starter for AI-901 Obj 2 Part VI (Computer Vision & Image Generation). Two scripts:

- `src/analyze_image.py` — calls Azure AI Vision `ImageAnalysisClient.analyze()` on `sample_data/retail_shelf.jpg` and prints captions, tags, objects, OCR lines.
- `src/generate_image.py` — calls the Foundry image-generation deployment (e.g. DALL·E 3) for a hard-coded prompt and saves the PNG next to the script.

Exercise extends both: adds multimodal chat (send image + question to a chat model via `azure-ai-inference`), adds OCR-only mode, and swaps in different image-gen prompts with style guidance.

## What's here
- `src/analyze_image.py`, `src/generate_image.py`
- `sample_data/retail_shelf.jpg` — tiny placeholder image (replace with any retail shelf photo for a richer demo).
- `sample_data/PLACEHOLDER.md` — where to find better sample images.

## Env vars
Copy `.env.example` → `.env`. Fill in `VISION_ENDPOINT` (for analyze) and `FOUNDRY_PROJECT_ENDPOINT` + `IMAGE_GEN_DEPLOYMENT_NAME` (for generate).

## Run
```
python src/analyze_image.py
python src/generate_image.py
```
