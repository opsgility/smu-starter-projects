"""
Synthesize speech audio (output.wav) from text using Azure AI Speech.
"""
import os
import sys
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

KEY = os.environ["SPEECH_KEY"]
REGION = os.environ["SPEECH_REGION"]
VOICE = "en-US-AriaNeural"


def synthesize(text: str, out_path: Path) -> None:
    # TODO 1: build a SpeechConfig, set speech_synthesis_voice_name = VOICE.
    # TODO 2: build an AudioConfig using filename=str(out_path).
    # TODO 3: build a SpeechSynthesizer and call speak_text_async(text).get().
    # TODO 4: raise RuntimeError if reason != ResultReason.SynthesizingAudioCompleted.
    raise NotImplementedError


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "Welcome to Northwind Horizon."
    synthesize(text, Path("output.wav"))
    print("Wrote output.wav")
