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
    # TODO (Exercise 3 Step 7 - TODO 1): build a SpeechConfig via ``_config()``,
    # set ``speech_synthesis_voice_name = "en-US-JennyNeural"`` and
    # ``set_speech_synthesis_output_format(SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)``,
    # create an AudioOutputConfig with ``filename=str(out_path)``, instantiate
    # a SpeechSynthesizer, and call ``speak_text_async(text).get()``. Raise
    # RuntimeError if ``result.reason != SynthesizingAudioCompleted`` including
    # ``result.cancellation_details.error_details`` in the message. Return
    # ``out_path``.
    raise NotImplementedError("Exercise 3 TODO 1: synthesize (TTS)")


def transcribe(audio_path: Path) -> str:
    """One-shot STT: transcribe a short utterance and return the recognized text.

    Speech SDK expects 16 kHz / 16-bit mono PCM WAV. If STT returns NoMatch,
    inspect the WAV with ``ffprobe`` and convert with
    ``ffmpeg -i in.wav -ar 16000 -ac 1 -sample_fmt s16 fixed.wav``.
    """
    # TODO (Exercise 3 Step 8 - TODO 2): build a SpeechConfig
    # (``speechsdk.SpeechConfig(subscription=KEY, region=REGION)``), build an
    # AudioConfig with ``filename=str(audio_path)``, create a SpeechRecognizer,
    # and call ``recognize_once_async().get()``. Raise RuntimeError if
    # ``result.reason != RecognizedSpeech``. Return ``result.text``.
    raise NotImplementedError("Exercise 3 TODO 2: transcribe (STT)")


def translate_speech(audio_path: Path, target_lang: str) -> dict:
    """Speech-in / translated-text-out via ``TranslationRecognizer``.

    Returns ``{"source_text": <recognized English>, "translations": {<lang>: <text>}}``.
    """
    # TODO (Exercise 3 Step 9 - TODO 3): build a
    # ``speechsdk.translation.SpeechTranslationConfig(subscription=KEY, region=REGION)``,
    # set ``speech_recognition_language = "en-US"``, call
    # ``add_target_language(target_lang)``, build an AudioConfig from
    # ``audio_path``, create a TranslationRecognizer, and call
    # ``recognize_once_async().get()``. Accept either ``TranslatedSpeech`` or
    # ``RecognizedSpeech`` as success. Return
    # ``{"source_text": result.text, "translations": dict(result.translations)}``.
    raise NotImplementedError("Exercise 3 TODO 3: translate_speech")
