"""
Transcribe a WAV file using Azure AI Speech.
"""
import os
import sys
from pathlib import Path

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

KEY = os.environ["SPEECH_KEY"]
REGION = os.environ["SPEECH_REGION"]
HERE = Path(__file__).parent
DEFAULT_INPUT = HERE / "sample_data" / "question.wav"


def transcribe(path: Path) -> str:
    # TODO 1: build a SpeechConfig from KEY and REGION.
    # TODO 2: build an AudioConfig from the WAV path.
    # TODO 3: build a SpeechRecognizer with the speech config + audio config.
    # TODO 4: call recognizer.recognize_once_async().get() and return result.text on success.
    #         Raise RuntimeError if result.reason != ResultReason.RecognizedSpeech.
    raise NotImplementedError


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    print(transcribe(path))
