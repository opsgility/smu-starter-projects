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


if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: Token-by-Token Streaming")
    print("=" * 50)
    # stream_response("Explain Python decorators in 3 sentences.")  # Uncomment after implementing Exercise 1

    # Uncomment when you reach Exercise 1 Step 4:
    # print("\n" + "=" * 50)
    # print("Exercise 1 Step 4: Stream with Usage Stats")
    # print("=" * 50)
    # text, stats = stream_with_stats("Explain Python decorators in 3 sentences.")
    # print(stats)

    # Uncomment when you reach Exercise 2:
    # print("\n" + "=" * 50)
    # print("Exercise 2: Time-to-First-Token Across Models")
    # print("=" * 50)
    # for model in ["gpt-4.1-nano", "gpt-4.1-mini", "gpt-4.1"]:
    #     result = timed_stream("Explain Python decorators in 3 sentences.", model=model)
    #     print(result)

    # Uncomment when you reach Exercise 3:
    # print("\n" + "=" * 50)
    # print("Exercise 3: Streaming vs Non-Streaming")
    # print("=" * 50)
    # compare_streaming(
    #     "Explain how TCP/IP handshakes work in detail, including SYN, SYN-ACK, ACK phases, with a diagram in ASCII."
    # )
