"""
Streaming Completions with the OpenAI Responses API
Course 101 - Lesson 6: Streaming Terminal Assistant

Exercises:
1. Stream a response token-by-token and capture usage stats
2. Measure time-to-first-token (TTFT) across models
3. Compare streaming vs non-streaming latency

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
import time
from openai import OpenAI

client = OpenAI()


def stream_response(prompt: str, model: str = "gpt-4.1-mini") -> str:
    """
    TODO (Exercise 1): Use client.responses.stream(model=model, input=prompt) as a
    context manager. Iterate events with `for event in stream`, filter on
    event.type == "response.output_text.delta", and print event.delta with end=''
    and flush=True. Return the full concatenated text.
    """
    pass


def stream_with_stats(prompt: str) -> tuple[str, dict]:
    """
    TODO (Exercise 1, Step 4): Like stream_response, but after the event loop call
    stream.get_final_response() to capture usage. Return (full_text, stats_dict)
    where stats_dict has keys: input_tokens, output_tokens, total_tokens.
    """
    pass


def timed_stream(prompt: str, model: str = "gpt-4.1-mini") -> dict:
    """
    TODO (Exercise 2): Stream a response and measure time-to-first-token (TTFT).
    Record start time, capture first_token_time on the first
    response.output_text.delta event, capture end time after the stream completes.
    Return a dict: {model, ttft_seconds, total_seconds, delta_events}.
    """
    pass


def compare_streaming(prompt: str) -> None:
    """
    TODO (Exercise 3): Time a non-streaming call (client.responses.create) end-to-end,
    then time a streaming call capturing first_token_time on the first
    response.output_text.delta event. Print both latencies and a line like
    'Streaming advantage: first token {X:.1f}x sooner'.
    """
    pass


if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: Token-by-Token Streaming")
    print("=" * 50)
    stream_response("Explain Python decorators in 3 sentences.")

    print("\n" + "=" * 50)
    print("Exercise 1 Step 4: Stream with Usage Stats")
    print("=" * 50)
    text, stats = stream_with_stats("Explain Python decorators in 3 sentences.")
    print(stats)

    print("\n" + "=" * 50)
    print("Exercise 2: Time-to-First-Token Across Models")
    print("=" * 50)
    for model in ["gpt-4.1-nano", "gpt-4.1-mini", "gpt-4.1"]:
        result = timed_stream("Explain Python decorators in 3 sentences.", model=model)
        print(result)

    print("\n" + "=" * 50)
    print("Exercise 3: Streaming vs Non-Streaming")
    print("=" * 50)
    compare_streaming(
        "Explain how TCP/IP handshakes work in detail, including SYN, SYN-ACK, ACK phases, with a diagram in ASCII."
    )
