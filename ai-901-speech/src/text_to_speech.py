"""Synthesize a fixed phrase to output.wav."""
from __future__ import annotations

import os

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

KEY = os.environ.get("SPEECH_KEY")
REGION = os.environ.get("SPEECH_REGION", "eastus2")

PHRASE = "Hello from Northwind Horizon. How can I help you today?"
VOICE = "en-US-JennyNeural"


def main() -> None:
    if not KEY:
        raise SystemExit("Set SPEECH_KEY / SPEECH_REGION in .env.")
    cfg = speechsdk.SpeechConfig(subscription=KEY, region=REGION)
    cfg.speech_synthesis_voice_name = VOICE
    audio_out = speechsdk.audio.AudioOutputConfig(filename="output.wav")
    synth = speechsdk.SpeechSynthesizer(speech_config=cfg, audio_config=audio_out)
    result = synth.speak_text_async(PHRASE).get()
    print(f"synthesized reason={result.reason} → output.wav")


if __name__ == "__main__":
    main()
