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
    # TODO (Exercise 3 Step 3): construct SpeechConfig(subscription=KEY, region=REGION),
    # set cfg.speech_synthesis_voice_name = VOICE, and return it.
    raise NotImplementedError(
        "Complete TODOs in app/speech.py (Exercise 3 Step 3)."
    )


def synthesize(text: str, out_path: Path) -> Path:
    """TTS: write ``text`` as a WAV file at ``out_path`` and return that path."""
    with tracer.start_as_current_span("summitline.speech.synthesize") as span:
        span.set_attribute("text.chars", len(text))
        span.set_attribute("out_path", str(out_path))

        # TODO (Exercise 3 Step 3): build AudioOutputConfig(filename=str(out_path)),
        # instantiate SpeechSynthesizer(speech_config=_cfg(), audio_config=audio),
        # call synth.speak_text_async(text).get(), verify
        # result.reason == ResultReason.SynthesizingAudioCompleted, return out_path.
        raise NotImplementedError(
            "Complete TODOs in app/speech.py (Exercise 3 Step 3)."
        )


def transcribe(audio_path: Path) -> str:
    """STT: return the recognized text from a WAV file at ``audio_path``."""
    with tracer.start_as_current_span("summitline.speech.transcribe") as span:
        span.set_attribute("audio_path", str(audio_path))

        # TODO (Exercise 3 Step 3): build AudioConfig(filename=str(audio_path)),
        # SpeechRecognizer(speech_config=_cfg(), audio_config=audio),
        # call rec.recognize_once_async().get(), verify
        # result.reason == ResultReason.RecognizedSpeech, return result.text.
        raise NotImplementedError(
            "Complete TODOs in app/speech.py (Exercise 3 Step 3)."
        )
