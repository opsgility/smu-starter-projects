"""Transcribe audio from a file or the default microphone."""
from __future__ import annotations

import argparse
import os

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

KEY = os.environ.get("SPEECH_KEY")
REGION = os.environ.get("SPEECH_REGION", "eastus2")


def recognize_from_file(path: str) -> str:
    cfg = speechsdk.SpeechConfig(subscription=KEY, region=REGION)
    audio = speechsdk.audio.AudioConfig(filename=path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=cfg, audio_config=audio)
    result = recognizer.recognize_once_async().get()
    return result.text or f"(no speech recognized, reason={result.reason})"


def recognize_from_mic() -> str:
    cfg = speechsdk.SpeechConfig(subscription=KEY, region=REGION)
    recognizer = speechsdk.SpeechRecognizer(speech_config=cfg)
    print("Speak now…")
    result = recognizer.recognize_once_async().get()
    return result.text or f"(no speech recognized, reason={result.reason})"


def main() -> None:
    if not KEY:
        raise SystemExit("Set SPEECH_KEY / SPEECH_REGION in .env.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="WAV file path")
    parser.add_argument("--mic", action="store_true", help="Record from default mic")
    args = parser.parse_args()
    text = recognize_from_mic() if args.mic else recognize_from_file(args.file or "sample_data/hello.wav")
    print(f"transcript: {text}")


if __name__ == "__main__":
    main()
