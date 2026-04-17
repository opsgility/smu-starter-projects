# AI-901 Lesson 10 — Content Understanding Starter

Scaffold for Lesson 10. You'll use **Azure Content Understanding** (in Foundry Tools) to extract structured information from documents, images, audio, and video. Content Understanding is a REST-based service so this starter uses `requests` rather than an SDK.

## Files

- `analyzer.py` — shared helpers: create an analyzer, submit content, poll for results
- `extract_document.py` — extract fields from an invoice PDF
- `extract_image.py` — extract data from a receipt image
- `extract_audio.py` — extract from a call recording (WAV)
- `extract_video.py` — extract from a short MP4
- `schemas/` — JSON schemas defining what fields to extract for each asset type
- `sample_data/` — sample PDFs / images / audio (drop your own during the lab)
