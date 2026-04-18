# AI-103 Lesson 12 — Text Analysis + Speech Starter

Two endpoint families:
- **Text** — structured JSON extraction (LLM), sentiment + key phrases (Language), translation (Translator)
- **Speech** — TTS, STT, voice-in / voice-out agent loop, speech translation

## Files

- `app/text.py`      — entity / sentiment / extraction / translation
- `app/speech.py`    — STT + TTS helpers
- `app/translate.py` — Translator REST wrapper
- `app/main.py`      — FastAPI exposing /analyze, /summarize, /translate, /speak, /transcribe, /voice-agent

## Run

```bash
pip install -r requirements.txt
cp .env.example .env
az login
uvicorn app.main:app --reload --port 8000
```
