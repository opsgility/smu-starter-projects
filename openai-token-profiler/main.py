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


def count_tokens(text: str, model: str = "gpt-4.1") -> int:
    """
    TODO (Exercise 1): Use tiktoken.encoding_for_model(model) to get the encoder,
    then return len(encoding.encode(text)). Fall back to cl100k_base if the model
    isn't directly recognized.
    """
    pass


def calculate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """
    TODO (Exercise 2): Look up PRICING[model], compute
    (input_tokens / 1_000_000) * pricing['input'] + (output_tokens / 1_000_000) * pricing['output'],
    and return the total USD cost as a float.
    """
    pass


def benchmark_model(model: str, prompt: str) -> dict:
    """
    TODO (Exercise 3): Call client.responses.create(model=model, input=prompt),
    measure latency in seconds, and return:
    {
      'model': model,
      'latency_seconds': round(latency, 3),
      'input_tokens': response.usage.input_tokens,
      'output_tokens': response.usage.output_tokens,
      'total_tokens': response.usage.total_tokens,
      'cost_usd': calculate_cost(...),
      'answer_preview': response.output_text[:60],
    }
    """
    pass


def run_benchmark() -> None:
    """
    TODO (Exercise 3): For each model in ['gpt-4.1-nano', 'gpt-4.1-mini', 'gpt-4.1']
    and each prompt in a hardcoded list (3 prompts of varying complexity), call
    benchmark_model and print a formatted table with columns: Model, Latency (s),
    Input Tokens, Output Tokens, Cost, Preview.
    """
    pass


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

    print("\n" + "=" * 60)
    print("Exercise 2: Cost Calculation")
    print("=" * 60)
    # cost = calculate_cost(100, 200, "gpt-4.1-mini")  # Uncomment after implementing Exercise 2
    # print(f"Cost for 100 input + 200 output tokens on gpt-4.1-mini: ${cost:.6f}")

    print("\n" + "=" * 60)
    print("Exercise 3: Model Benchmark Comparison")
    print("=" * 60)
    # run_benchmark()  # Uncomment after implementing Exercise 3
