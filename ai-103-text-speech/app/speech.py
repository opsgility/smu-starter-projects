"""Azure Speech SDK helpers for the Summitline in-store voice kiosk.

Exercise 3 implements three helpers:

- ``synthesize(text, out_path)``           — text-to-speech (TTS).
- ``transcribe(audio_path)``               — speech-to-text (STT).
- ``translate_speech(audio_path, target)`` — speech translation.

All three helpers build on the same ``SpeechConfig`` (subscription + region).
The Speech SDK only exposes async methods; the standard pattern is
``some_async(...).get()`` to block until the result is ready.
"""

from __future__ import annotations

import os
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Environment wiring.
# ---------------------------------------------------------------------------
KEY = os.environ["SPEECH_KEY"]
REGION = os.environ["SPEECH_REGION"]


def _config() -> speechsdk.SpeechConfig:
    """Shared factory so every helper starts from the same auth config."""
    return speechsdk.SpeechConfig(subscription=KEY, region=REGION)


def synthesize(text: str, out_path: Path) -> Path:
    """Synthesize ``text`` to a WAV file at ``out_path`` and return the path.

    Uses ``en-US-JennyNeural`` and ``Riff24Khz16BitMonoPcm`` so the resulting
    WAV is browser-playable for the kiosk front-end.
    """
    # Exercise 3 - Step 7 Start
    raise NotImplementedError("Complete Exercise 3 Step 7")
    # Exercise 3 - Step 7 End


def transcribe(audio_path: Path) -> str:
    """One-shot STT: transcribe a short utterance and return the recognized text.

    Speech SDK expects 16 kHz / 16-bit mono PCM WAV. If STT returns NoMatch,
    inspect the WAV with ``ffprobe`` and convert with
    ``ffmpeg -i in.wav -ar 16000 -ac 1 -sample_fmt s16 fixed.wav``.
    """
    # Exercise 3 - Step 8 Start
    raise NotImplementedError("Complete Exercise 3 Step 8")
    # Exercise 3 - Step 8 End


def translate_speech(audio_path: Path, target_lang: str) -> dict:
    """Speech-in / translated-text-out via ``TranslationRecognizer``.

    Returns ``{"source_text": <recognized English>, "translations": {<lang>: <text>}}``.
    """
    # Exercise 3 - Step 9 Start
    raise NotImplementedError("Complete Exercise 3 Step 9")
    # Exercise 3 - Step 9 End
