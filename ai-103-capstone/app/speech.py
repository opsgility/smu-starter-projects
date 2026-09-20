"""/voice — Speech SDK STT and TTS helpers (Exercise 3)."""

from __future__ import annotations

import os
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from opentelemetry import trace

KEY = os.environ.get("SPEECH_KEY", "")
REGION = os.environ.get("SPEECH_REGION", "eastus2")
VOICE = os.environ.get("SPEECH_VOICE", "en-US-JennyNeural")

tracer = trace.get_tracer("summitline-capstone")


def _cfg() -> "speechsdk.SpeechConfig":
    """Build a ``SpeechConfig`` with the Summitline default voice.

    Helper — TODO 1/2 in Exercise 3 Step 3 fills in the body.
    """
    # Exercise 3 - Step 3 Start
    raise NotImplementedError("Complete Exercise 3 Step 3")
    # Exercise 3 - Step 3 End


def synthesize(text: str, out_path: Path) -> Path:
    """TTS: write ``text`` as a WAV file at ``out_path`` and return that path."""
    with tracer.start_as_current_span("summitline.speech.synthesize") as span:
        span.set_attribute("text.chars", len(text))
        span.set_attribute("out_path", str(out_path))

        # Exercise 3 - Step 3 Start
        raise NotImplementedError("Complete Exercise 3 Step 3")
        # Exercise 3 - Step 3 End


def transcribe(audio_path: Path) -> str:
    """STT: return the recognized text from a WAV file at ``audio_path``."""
    with tracer.start_as_current_span("summitline.speech.transcribe") as span:
        span.set_attribute("audio_path", str(audio_path))

        # Exercise 3 - Step 3 Start
        raise NotImplementedError("Complete Exercise 3 Step 3")
        # Exercise 3 - Step 3 End
