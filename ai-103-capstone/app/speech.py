"""Capstone speech — TTS + STT."""
import os
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

KEY = os.environ["SPEECH_KEY"]
REGION = os.environ["SPEECH_REGION"]
VOICE = "en-US-AriaNeural"


def synthesize(text: str, out_path: Path) -> Path:
    # TODO 1: SpeechConfig + voice + AudioOutputConfig(filename) + SpeechSynthesizer.
    # TODO 2: speak_text_async(text).get(); raise on failure; return out_path.
    raise NotImplementedError


def transcribe(audio_path: Path) -> str:
    # TODO 3: SpeechConfig + AudioConfig(filename) + SpeechRecognizer.
    # TODO 4: recognize_once_async().get(); raise on failure; return result.text.
    raise NotImplementedError
