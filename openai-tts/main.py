"""
Text-to-Speech with OpenAI TTS
Course 203 - Lesson 6: TTS Exercises

Exercises:
1. Generate speech with tts-1 and save to file
2. Compare all 6 built-in voices
3. Use gpt-4o-mini-tts with style instructions for expressive speech
4. Stream audio for low-latency playback

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
import os
import time

client = OpenAI()

# Available voices for tts-1 and tts-1-hd
VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

# Sample texts
SAMPLE_TEXT = "Welcome to the OpenAI text-to-speech API. This voice was generated using advanced neural speech synthesis."
NEWS_TEXT = "Breaking news: Scientists have discovered a new species of deep-sea fish in the Pacific Ocean, glowing with bioluminescent patterns never seen before."
CUSTOMER_SERVICE_TEXT = "Thank you for calling support. Your ticket number is 12345. Our team will respond within 24 hours."


# -----------------------------------------------------------------------
# Exercise 1: Basic TTS
# -----------------------------------------------------------------------

def generate_speech(text: str, voice: str = "alloy", output_path: str = "output.mp3") -> str:
    """
    Exercise 1: Generate speech from text using tts-1.

    Use client.audio.speech.create() with:
    - model="tts-1"
    - voice=voice
    - input=text

    Save the audio to output_path using response.stream_to_file().

    Returns:
        output_path (the saved file path)
    """
    # TODO: Call client.audio.speech.create(
    #   model="tts-1",
    #   voice=voice,
    #   input=text
    # )
    # TODO: Call response.stream_to_file(output_path)
    # TODO: Return output_path
    pass


# -----------------------------------------------------------------------
# Exercise 2: Voice comparison
# -----------------------------------------------------------------------

def compare_voices(text: str) -> dict[str, str]:
    """
    Exercise 2: Generate the same text with all 6 voices.

    Loop over VOICES, calling generate_speech() for each.
    Save each to f"{voice}_sample.mp3".

    Returns:
        Dict mapping voice name to file path
        e.g. {"alloy": "alloy_sample.mp3", "echo": "echo_sample.mp3", ...}
    """
    results = {}
    # TODO: Loop over VOICES
    # TODO: Call generate_speech(text, voice=v, output_path=f"{v}_sample.mp3")
    # TODO: Add to results dict
    # TODO: Print timing info for each voice
    return results


# -----------------------------------------------------------------------
# Exercise 3: Expressive speech with gpt-4o-mini-tts
# -----------------------------------------------------------------------

def generate_expressive_speech(text: str, style_instructions: str,
                                output_path: str = "expressive.mp3") -> str:
    """
    Exercise 3: Generate expressive speech with style instructions.

    gpt-4o-mini-tts supports a 'instructions' parameter that controls
    speaking style, emotion, pace, and tone.

    Use client.audio.speech.create() with:
    - model="gpt-4o-mini-tts"
    - voice="alloy"
    - input=text
    - instructions=style_instructions

    Returns:
        output_path
    """
    # TODO: Call client.audio.speech.create(
    #   model="gpt-4o-mini-tts",
    #   voice="alloy",
    #   input=text,
    #   instructions=style_instructions
    # )
    # TODO: Call response.stream_to_file(output_path)
    # TODO: Return output_path
    pass


# -----------------------------------------------------------------------
# Exercise 4: Streaming audio
# -----------------------------------------------------------------------

def stream_speech(text: str, output_path: str = "streamed.mp3") -> float:
    """
    Exercise 4: Stream audio with low latency using iter_bytes().

    Instead of stream_to_file(), iterate over chunks directly
    using response.iter_bytes(chunk_size=4096).

    This allows processing/playing audio chunks as they arrive
    rather than waiting for the full file.

    Measure and return the time to first byte (seconds).

    Use:
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=text
    ) as response:
        for chunk in response.iter_bytes(chunk_size=4096):
            # process chunk
            ...

    Returns:
        Time to first chunk in seconds
    """
    start = time.time()
    first_chunk_time = None

    # TODO: Use client.audio.speech.with_streaming_response.create()
    # TODO: Iterate response.iter_bytes(chunk_size=4096)
    # TODO: Record time.time() - start on first chunk
    # TODO: Write all chunks to output_path
    # TODO: Return first_chunk_time

    return first_chunk_time or 0.0


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

if __name__ == "__main__":
    print("Text-to-Speech Exercises")
    print("=" * 60)

    # Exercise 1
    print("\nExercise 1: Basic Speech Generation")
    path = generate_speech(SAMPLE_TEXT, voice="alloy", output_path="basic_speech.mp3")
    if path and os.path.exists(path):
        size = os.path.getsize(path)
        print(f"  Saved to: {path} ({size:,} bytes)")

    # Exercise 2
    print("\nExercise 2: Voice Comparison (6 voices)")
    voice_files = compare_voices("Hello, I am an AI assistant. How can I help you today?")
    for voice, filepath in voice_files.items():
        if filepath and os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"  {voice:8s}: {filepath} ({size:,} bytes)")

    # Exercise 3
    print("\nExercise 3: Expressive Speech")
    styles = [
        ("excited_news.mp3", NEWS_TEXT, "Speak like an excited news anchor, fast-paced and enthusiastic."),
        ("calm_support.mp3", CUSTOMER_SERVICE_TEXT, "Speak slowly and calmly, like a patient customer service representative."),
    ]
    for filename, text, instructions in styles:
        path = generate_expressive_speech(text, instructions, output_path=filename)
        if path and os.path.exists(path):
            print(f"  Style: {instructions[:50]}...")
            print(f"  Saved: {path} ({os.path.getsize(path):,} bytes)")

    # Exercise 4
    print("\nExercise 4: Streaming Audio")
    ttfb = stream_speech(SAMPLE_TEXT, output_path="streamed_speech.mp3")
    print(f"  Time to first byte: {ttfb:.3f}s")
    if os.path.exists("streamed_speech.mp3"):
        print(f"  Streamed file size: {os.path.getsize('streamed_speech.mp3'):,} bytes")
