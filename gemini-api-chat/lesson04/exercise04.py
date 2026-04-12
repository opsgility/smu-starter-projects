#!/usr/bin/env python3
"""
Lesson 4, Exercise 4: Complete Chat Application

Combine everything from exercises 1-3 into a single interactive terminal app:
- Multi-turn conversation with history (Exercise 1)
- Image analysis via URL (Exercise 2)
- Function calling for weather + currency (Exercise 3)
- Streaming responses for all text output

TODO: Build the main() loop and helper functions.
The command interface is defined below — implement the logic.
"""
import os
import time
import requests
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from google.generativeai.types import FunctionDeclaration, Tool

genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))


# ─── Reuse your implementations from exercises 1-3 ───────────────────────────
# Copy (or import) your completed functions from exercise01, 02, and 03
# OR re-implement them here. The choice is yours.

def get_weather(city: str) -> dict:
    """From exercise03 — simulated weather data."""
    data = {
        "London":   {"temperature_c": 12, "condition": "Cloudy"},
        "Tokyo":    {"temperature_c": 22, "condition": "Sunny"},
        "New York": {"temperature_c": 18, "condition": "Partly Cloudy"},
        "Sydney":   {"temperature_c": 25, "condition": "Sunny"},
    }
    return {"city": city, **data.get(city, {"temperature_c": 20, "condition": "Unknown"})}


def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """From exercise03 — simulated currency conversion."""
    rates = {"USD": 1.0, "EUR": 0.92, "GBP": 0.79, "JPY": 149.5}
    fc, tc = from_currency.upper(), to_currency.upper()
    if fc not in rates or tc not in rates:
        return {"error": "Unsupported currency"}
    converted = amount * (rates[tc] / rates[fc])
    return {"original": f"{amount} {fc}", "converted": f"{converted:.2f} {tc}"}


def load_image_from_url(url: str) -> Image.Image:
    """From exercise02 — load PIL Image from URL."""
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return Image.open(BytesIO(r.content))


# TODO: Set up the tools (FunctionDeclaration + Tool) from exercise03
# TODO: Create model_with_tools = genai.GenerativeModel('gemini-2.0-flash', tools=[...])
# TODO: Create a chat session using model_with_tools.start_chat()


def stream_print(prompt_or_parts) -> str:
    """
    TODO: Send a message via the chat session with stream=True.
    Print each chunk as it arrives (print(chunk.text, end='', flush=True)).
    Return the complete aggregated text.
    Hint: use chat.send_message(prompt_or_parts, stream=True)
    """
    pass


def handle_image_command(url: str) -> None:
    """
    TODO: Load the image from the URL, then ask Gemini to describe it.
    Stream the response using stream_print().
    Handle errors (invalid URL, network error) gracefully.
    """
    pass


def handle_function_call_response(response) -> str:
    """
    TODO: If the response contains a function call, execute it and return
    the final text answer after sending the result back to Gemini.
    If no function call, return response.text directly.
    Reuse the pattern from exercise03.
    """
    pass


def print_help():
    print("""
Commands:
  /image <url>         Analyze an image from a URL
  /weather <city>      Get weather (uses function calling)
  /convert <n> <from> <to>  Convert currency (e.g. /convert 100 USD EUR)
  /history             Show conversation history
  /clear               Start a new conversation
  /help                Show this help
  /quit                Exit

Or just type anything to chat with Gemini!
""")


def main():
    print("=" * 55)
    print("  Gemini AI Chat Application")
    print("=" * 55)
    print_help()

    # TODO: Main interaction loop
    # For each command:
    # /image <url>      → handle_image_command(url)
    # /weather <city>   → chat_with_tools(f"What is the weather in {city}?")
    # /convert <n> <f> <t> → chat_with_tools(f"Convert {n} {f} to {t}")
    # /history          → display conversation history
    # /clear            → reset chat session
    # /help             → print_help()
    # /quit             → break
    # anything else     → stream_print(user_input)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        # TODO: Implement command routing here
        pass


if __name__ == '__main__':
    main()
