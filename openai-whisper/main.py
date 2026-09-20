"""
Audio Transcription with Whisper
Course 203 - Lesson 4: Whisper Exercises

Exercises:
1. Transcribe an audio file with Whisper
2. Get word-level timestamps from transcription
3. Translate audio to English
4. Route voice commands to different handlers based on transcription

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
from pydantic import BaseModel
import json
import os

client = OpenAI()

# Sample audio file for exercises (provided in lab environment)
SAMPLE_AUDIO_PATH = "sample_audio.mp3"
SAMPLE_SPANISH_AUDIO_PATH = "sample_spanish.mp3"

# Voice command handlers
COMMAND_HANDLERS = {
    "weather": lambda cmd: f"Fetching weather for: {cmd}",
    "reminder": lambda cmd: f"Setting reminder: {cmd}",
    "search": lambda cmd: f"Searching for: {cmd}",
    "calculation": lambda cmd: f"Calculating: {cmd}",
    "unknown": lambda cmd: f"Unknown command: {cmd}",
}


# -----------------------------------------------------------------------
# Exercise 1: Basic transcription
# -----------------------------------------------------------------------

def transcribe_audio(audio_path: str) -> str:
    """
    Exercise 1: Transcribe an audio file using Whisper.

    Use client.audio.transcriptions.create() with:
    - model="whisper-1"
    - file=open(audio_path, "rb")

    Returns:
        The transcribed text string (transcription.text)
    """
    with open(audio_path, "rb") as f:
        # TODO: Call client.audio.transcriptions.create(
        #   model="whisper-1",
        #   file=f
        # )
        # TODO: Return transcription.text
        pass


# -----------------------------------------------------------------------
# Exercise 2: Timestamps
# -----------------------------------------------------------------------

def transcribe_with_timestamps(audio_path: str) -> dict:
    """
    Exercise 2: Transcribe audio and get word-level timestamps.

    Add these parameters to client.audio.transcriptions.create():
    - response_format="verbose_json"
    - timestamp_granularities=["word"]

    The response includes:
    - transcription.text — full text
    - transcription.words — list of word objects with start/end times
    - transcription.duration — total audio duration in seconds

    Returns:
        Dict with keys: text, words, duration
        Each word: {"word": str, "start": float, "end": float}
    """
    with open(audio_path, "rb") as f:
        # TODO: Call client.audio.transcriptions.create() with:
        #   model="whisper-1"
        #   file=f
        #   response_format="verbose_json"
        #   timestamp_granularities=["word"]
        # TODO: Return {"text": ..., "words": [...], "duration": ...}
        pass


# -----------------------------------------------------------------------
# Exercise 3: Translation
# -----------------------------------------------------------------------

def translate_audio_to_english(audio_path: str) -> str:
    """
    Exercise 3: Translate non-English audio to English.

    Use client.audio.translations.create() (NOT transcriptions).
    Parameters:
    - model="whisper-1"
    - file=open(audio_path, "rb")

    The translations endpoint always outputs English regardless
    of the source language.

    Returns:
        English translation text (translation.text)
    """
    with open(audio_path, "rb") as f:
        # TODO: Call client.audio.translations.create(
        #   model="whisper-1",
        #   file=f
        # )
        # TODO: Return translation.text
        pass


# -----------------------------------------------------------------------
# Exercise 4: Voice command routing
# -----------------------------------------------------------------------

class CommandRoute(BaseModel):
    command_type: str   # weather, reminder, search, calculation, unknown
    parameters: str     # extracted parameters for the command
    confidence: float   # 0.0 to 1.0


def classify_voice_command(transcript: str) -> CommandRoute:
    """
    Exercise 4a: Use GPT-4.1-mini to classify a voice command transcript.

    System prompt: "You are a voice command classifier. Identify the command
    type and extract relevant parameters."

    Use client.responses.parse() with text_format=CommandRoute.

    Valid command_type values: weather, reminder, search, calculation, unknown

    Returns:
        CommandRoute with command_type, parameters, and confidence
    """
    system = """You are a voice command classifier. Identify the command type and
extract relevant parameters. Command types: weather, reminder, search, calculation, unknown."""

    # TODO: Call client.responses.parse() with:
    #   model="gpt-4.1-mini"
    #   input=[system message, user message with transcript]
    #   text_format=CommandRoute
    # TODO: Return response.output_parsed
    pass


def process_voice_command(audio_path: str) -> dict:
    """
    Exercise 4b: Full voice command pipeline.
    1. Transcribe the audio
    2. Classify the command
    3. Route to the appropriate handler
    4. Return the result

    Returns:
        Dict with: transcript, command_type, parameters, result
    """
    # TODO: Call transcribe_audio(audio_path) to get transcript
    # TODO: Call classify_voice_command(transcript) to get route
    # TODO: Get handler from COMMAND_HANDLERS[route.command_type]
    # TODO: Call handler(route.parameters) to get result
    # TODO: Return dict with transcript, command_type, parameters, result
    pass


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

if __name__ == "__main__":
    print("Whisper Audio Transcription Exercises")
    print("=" * 60)

    # Exercise 1
    if os.path.exists(SAMPLE_AUDIO_PATH):
        print("\nExercise 1: Basic Transcription")
        text = transcribe_audio(SAMPLE_AUDIO_PATH)
        if text:
            print(f"Transcript: {text}")

        # Exercise 2
        print("\nExercise 2: Transcription with Timestamps")
        result = transcribe_with_timestamps(SAMPLE_AUDIO_PATH)
        if result:
            print(f"Duration: {result.get('duration', 0):.1f}s")
            words = result.get("words", [])
            print(f"Word count: {len(words)}")
            if words:
                print(f"First word: '{words[0]['word']}' at {words[0]['start']:.2f}s")

        # Exercise 4
        print("\nExercise 4: Voice Command Routing")
        cmd_result = process_voice_command(SAMPLE_AUDIO_PATH)
        if cmd_result:
            print(f"Transcript: {cmd_result.get('transcript')}")
            print(f"Command: {cmd_result.get('command_type')}")
            print(f"Result: {cmd_result.get('result')}")
    else:
        print(f"\nNote: Place an MP3 file at '{SAMPLE_AUDIO_PATH}' to test exercises 1, 2, and 4.")

    # Exercise 3
    if os.path.exists(SAMPLE_SPANISH_AUDIO_PATH):
        print("\nExercise 3: Translation to English")
        translation = translate_audio_to_english(SAMPLE_SPANISH_AUDIO_PATH)
        if translation:
            print(f"English translation: {translation}")
    else:
        print(f"\nNote: Place a non-English MP3 at '{SAMPLE_SPANISH_AUDIO_PATH}' to test exercise 3.")
