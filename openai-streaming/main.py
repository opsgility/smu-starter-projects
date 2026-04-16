"""
Streaming Completions with the OpenAI Responses API
Course 101 - Lesson 6: Streaming Terminal Assistant

Exercises:
1. Stream a response token-by-token and render it live in the terminal
2. Show a progress indicator (elapsed time) while streaming
3. Verify that streaming output matches non-streaming output

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
import time
import sys

client = OpenAI()


def stream_response(prompt: str) -> str:
    """
    Exercise 1: Stream a response token-by-token.

    Use client.responses.stream() as a context manager.
    Iterate over stream.text_stream to get text deltas.
    Print each delta immediately using print(delta, end="", flush=True).
    After the stream completes, print a newline.
    Return the complete assembled text.

    Args:
        prompt: The user's input prompt

    Returns:
        The complete response text assembled from all deltas
    """
    print(f"Prompt: {prompt}")
    print("-" * 40)
    full_text = ""

    # TODO: Use 'with client.responses.stream(...) as stream:' context manager
    #   model = "gpt-4.1-mini"
    #   input = prompt
    # TODO: Iterate over stream.text_stream
    # TODO: For each text_delta: print it (end="", flush=True) and append to full_text
    # TODO: After the loop, print("\n") to end the line
    # TODO: Return full_text

    return full_text


def stream_with_timer(prompt: str) -> None:
    """
    Exercise 2: Stream a response while displaying elapsed time.

    Show a live timer in the terminal while tokens arrive.
    Update the timer display on the same line using carriage return (\r).
    After the stream completes, show "Done in X.Xs" and print the full response.

    Args:
        prompt: The user's input prompt
    """
    print(f"Streaming response for: '{prompt}'")

    start_time = time.time()
    full_text = ""

    # TODO: Use client.responses.stream() as a context manager
    # TODO: For each event in the stream:
    #   - Update elapsed = time.time() - start_time
    #   - Print to stderr: f"\r⏱  {elapsed:.1f}s" (sys.stderr, end="", flush=True)
    #   - If the event has text content, append it to full_text
    # TODO: After streaming, print the elapsed time and the full response
    pass


def compare_streaming_vs_nonstreaming(prompt: str) -> None:
    """
    Exercise 3: Verify streaming and non-streaming produce equivalent output.

    Make the same prompt to:
    1. The streaming API (using client.responses.stream())
    2. The non-streaming API (using client.responses.create())

    Compare the assembled streaming text against response.output_text.
    Print whether they match (normalized by stripping whitespace).

    Args:
        prompt: The prompt to test with both methods
    """
    print(f"Testing prompt: '{prompt}'")

    # TODO: Stream the response and assemble the full text
    streamed_text = ""
    # ... your streaming code here ...

    # TODO: Make a non-streaming call and get response.output_text
    nonstreamed_text = ""
    # ... your non-streaming code here ...

    # TODO: Compare the two (strip whitespace before comparing)
    # TODO: Print "MATCH" if they are equal, "MISMATCH" if not
    # TODO: Print both texts so the user can inspect them
    pass


if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: Token-by-Token Streaming")
    print("=" * 50)
    result = stream_response("Explain what a REST API is in 3 sentences.")
    print(f"\nAssembled text length: {len(result)} characters")

    print("\n" + "=" * 50)
    print("Exercise 2: Stream with Progress Timer")
    print("=" * 50)
    stream_with_timer("List 5 benefits of using a streaming API for chatbots.")

    print("\n" + "=" * 50)
    print("Exercise 3: Compare Streaming vs Non-Streaming")
    print("=" * 50)
    compare_streaming_vs_nonstreaming("What is the OpenAI Responses API in one sentence?")
