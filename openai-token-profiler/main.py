"""
Token Counting, Pricing & Cost Optimization
Course 101 - Lesson 8: Token Profiling & Model Selection

Exercises:
1. Count tokens using tiktoken before making an API call
2. Capture the usage object from responses and calculate cost
3. Benchmark GPT-4.1, GPT-4.1-mini, and GPT-4.1-nano on identical prompts

Pricing (as of April 2026 - verify at platform.openai.com/docs/pricing):
  GPT-4.1:       $2.00 / 1M input tokens,  $8.00 / 1M output tokens
  GPT-4.1-mini:  $0.40 / 1M input tokens,  $1.60 / 1M output tokens
  GPT-4.1-nano:  $0.10 / 1M input tokens,  $0.40 / 1M output tokens

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
import time
import tiktoken
from openai import OpenAI

client = OpenAI()

PRICING = {
    "gpt-4.1":      {"input": 2.00, "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
}


if __name__ == "__main__":
    print("=" * 60)
    print("Exercise 1: Token Counting with tiktoken")
    print("=" * 60)
    # for sample in [  # Uncomment after implementing Exercise 1
    #     "Hello, world!",
    #     "The quick brown fox jumps over the lazy dog.",
    #     "Analyze the CAP theorem and its implications for distributed systems design.",
    # ]:
    #     print(f"{count_tokens(sample)} tokens: {sample}")

    # Uncomment when you reach Exercise 2:
    # print("\n" + "=" * 60)
    # print("Exercise 2: Cost Calculation")
    # print("=" * 60)
    # cost = calculate_cost(100, 200, "gpt-4.1-mini")
    # print(f"Cost for 100 input + 200 output tokens on gpt-4.1-mini: ${cost:.6f}")

    # Uncomment when you reach Exercise 3:
    # print("\n" + "=" * 60)
    # print("Exercise 3: Model Benchmark Comparison")
    # print("=" * 60)
    # run_benchmark()
