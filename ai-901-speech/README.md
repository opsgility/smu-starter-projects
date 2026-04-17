# AI-901 Lesson 8 — Speech App Starter

Scaffold for Lesson 8. You'll build:

1. Speech-to-text — transcribe audio files using Azure AI Speech.
2. Text-to-speech — generate audio from text.
3. A small voice loop — transcribe the user, send the text to a Foundry chat model, speak the reply back.

## Files

- `speech_to_text.py` — transcribe `sample_data/question.wav`
- `text_to_speech.py` — synthesize `output.wav` from provided text
- `voice_loop.py` — transcribe → chat → synthesize pipeline
- `sample_data/question.wav` — sample audio (placeholder — record your own during the lab)
