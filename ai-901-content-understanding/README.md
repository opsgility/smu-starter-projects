# ai-901-content-understanding — Content Understanding REST scaffold

Starter for AI-901 Obj 2 Part VII (Information Extraction with Content Understanding).

Content Understanding is consumed via REST (no first-party SDK yet). This starter gives you a bearer-token helper plus three extraction stubs (document, image, audio).

## What's here
- `src/extract_document.py` — POSTs `sample_data/invoice.md` (or a real PDF) to an analyzer and polls until done.
- `src/extract_image.py` — extraction stub for `sample_data/receipt.jpg`.
- `src/extract_audio.py` — extraction stub for `sample_data/voicenote.wav`.
- `sample_data/invoice.md` — a plain-text stand-in for an invoice (see PLACEHOLDER).
- `sample_data/PLACEHOLDER.md` — instructions for dropping real sample assets.

## Env vars
Copy `.env.example` → `.env`. Fill in `CONTENT_UNDERSTANDING_ENDPOINT` and `ANALYZER_ID` (the exercise has you create the analyzer in Foundry Tools first).

## Run
```
python src/extract_document.py
```
