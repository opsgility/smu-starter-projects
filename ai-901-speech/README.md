# ai-901-speech — Azure Speech starter (STT + TTS)

Starter for AI-901 Obj 2 Part V (Speech AI with Foundry Tools). Plain speech-to-text and text-to-speech scaffolds. The exercise has you:

1. Transcribe a sample WAV.
2. Synthesize a reply to `output.wav` with a specific voice.
3. Chain STT → Foundry chat model → TTS (spoken prompt → spoken answer).

## What's here
- `src/speech_to_text.py` — transcribes `sample_data/hello.wav` (or use `--mic` to record 5 s from the default mic).
- `src/text_to_speech.py` — synthesizes a hard-coded phrase to `output.wav`.
- `sample_data/PLACEHOLDER.md` — instructions to drop a small WAV file here (the VS Code container does not ship one; exercise step 1 shows students how to generate one with TTS first).

## Env vars
Copy `.env.example` → `.env`. Set `SPEECH_KEY` and `SPEECH_REGION`.

Note: Speech SDK uses the key-based `SpeechConfig` constructor here for simplicity — the exercise also shows the token-based variant with `DefaultAzureCredential`.

## Run
```
python src/text_to_speech.py     # creates output.wav
python src/speech_to_text.py --file sample_data/hello.wav
```
