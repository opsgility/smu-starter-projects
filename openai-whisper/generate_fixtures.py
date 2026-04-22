"""
Generate audio fixtures for the Whisper lab using OpenAI TTS.
Idempotent: skips files that already exist.
Run automatically by startup.sh on lab boot.
"""
import os
from openai import OpenAI

FIXTURES = [
    {
        "path": "sample_audio.mp3",
        "voice": "alloy",
        "text": "Hello, this is a sample audio clip for testing the OpenAI Whisper transcription API. The quick brown fox jumps over the lazy dog.",
    },
    {
        "path": "sample_spanish.mp3",
        "voice": "nova",
        "text": "Hola, esta es una grabacion de prueba en espanol. El rapido zorro marron salta sobre el perro perezoso.",
    },
]


def main() -> None:
    client = OpenAI()
    for fx in FIXTURES:
        if os.path.exists(fx["path"]):
            print(f"[fixtures] {fx['path']} already exists, skipping")
            continue
        print(f"[fixtures] generating {fx['path']}...")
        response = client.audio.speech.create(
            model="tts-1",
            voice=fx["voice"],
            input=fx["text"],
        )
        response.stream_to_file(fx["path"])
        print(f"[fixtures] wrote {fx['path']}")


if __name__ == "__main__":
    main()
