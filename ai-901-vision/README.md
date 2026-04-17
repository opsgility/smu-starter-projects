# AI-901 Lesson 9 — Vision & Image Generation Starter

Scaffold for Lesson 9. You'll build:

1. **Vision input** — send an image to a multimodal Foundry model (gpt-4o) and ask it a question about the image.
2. **Image generation** — produce a new image from a text prompt using DALL-E 3 deployed in Foundry.
3. **Image analysis** — use Azure AI Vision `analyze` for tags, captions, and object detection on a local image.

## Files

- `vision_analyze.py` — multimodal image Q&A
- `image_generate.py` — text-to-image
- `vision_sdk.py` — Azure AI Vision analyze call
- `sample_data/storefront.jpg` — sample image (drop your own during the lab)
