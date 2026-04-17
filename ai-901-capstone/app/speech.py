"""Speech synthesis for /speak."""
import os
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

KEY = os.environ["SPEECH_KEY"]
REGION = os.environ["SPEECH_REGION"]
VOICE = "en-US-AriaNeural"


def synthesize(text: str, out_path: Path) -> Path:
    # TODO 1: build SpeechConfig, set speech_synthesis_voice_name = VOICE.
    # TODO 2: build AudioConfig(filename=str(out_path)) and a SpeechSynthesizer.
    # TODO 3: call speak_text_async(text).get(); raise on failure; return out_path.
    raise NotImplementedError
