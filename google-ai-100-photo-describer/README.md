# google-ai-100-photo-describer

Starter for **Google AI 100 — Lesson 4: Product-Photo Describer**.

You will describe Nimbus product photos with Gemini using `Part.from_uri` so
the model pulls images directly from Cloud Storage.

## Files

- `describe.py` — CLI skeleton
- `photos.json` — list of GCS URIs you will generate in Task 2 of the exercise
- `requirements.txt`

## Prep step (done during the exercise)

The exercise has you create a bucket `${PROJECT_ID}-nimbus-photos` in
us-central1 and upload 5 sample product photos (any JPEG/PNG of outdoor gear
works; the exercise provides a `gsutil cp` one-liner). You then populate
`photos.json` with their `gs://` URIs.
