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
from openai import OpenAI
import tiktoken
import time
from typing import NamedTuple

client = OpenAI()

# Pricing per 1M tokens (update from platform.openai.com/docs/pricing)
PRICING = {
    "gpt-4.1":      {"input": 2.00,  "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40,  "output": 1.60},
    "gpt-4.1-nano": {"input": 0.10,  "output": 0.40},
}


class BenchmarkResult(NamedTuple):
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cost_usd: float
    output_text: str


def count_tokens(text: str, model: str = "gpt-4.1-mini") -> int:
    """
    Exercise 1: Count tokens in a string before sending to the API.

    Use tiktoken to count how many tokens the given text will use.
    Use tiktoken.encoding_for_model() to get the right encoder.
    Return the token count as an integer.

    Args:
        text: The text to tokenize
        model: The model to use for tokenization

    Returns:
        Number of tokens
    """
    # TODO: Get the encoding for the model using tiktoken.encoding_for_model(model)
    # TODO: Encode the text using enc.encode(text)
    # TODO: Return len(tokens)
    return 0


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """
    Exercise 2: Calculate the USD cost of an API call.

    Use the PRICING dict above to compute cost.
    Formula: (input_tokens / 1_000_000) * input_price
           + (output_tokens / 1_000_000) * output_price

    Args:
        model: Model name (must be a key in PRICING)
        input_tokens: Number of input tokens used
        output_tokens: Number of output tokens used

    Returns:
        Cost in USD as a float
    """
    # TODO: Look up the model's input and output prices from PRICING
    # TODO: Calculate and return the total cost in USD
    return 0.0


def benchmark_model(model: str, prompt: str) -> BenchmarkResult:
    """
    Exercise 3a: Benchmark a single model on a given prompt.

    - Record start time before the API call
    - Make the Responses API call
    - Record end time after the API call
    - Capture input/output tokens from response.usage
    - Calculate cost using calculate_cost()
    - Return a BenchmarkResult

    Args:
        model: The model to benchmark
        prompt: The prompt to send

    Returns:
        BenchmarkResult with all metrics
    """
    # TODO: Record start = time.time()
    # TODO: Call client.responses.create(model=model, input=prompt)
    # TODO: Record end = time.time()
    # TODO: Calculate latency_ms = (end - start) * 1000
    # TODO: Get input_tokens = response.usage.input_tokens
    # TODO: Get output_tokens = response.usage.output_tokens
    # TODO: Calculate cost = calculate_cost(model, input_tokens, output_tokens)
    # TODO: Return BenchmarkResult(model, input_tokens, output_tokens, latency_ms, cost, response.output_text)
    pass


def run_benchmark(prompt: str) -> None:
    """
    Exercise 3b: Run the benchmark across all three model tiers.

    Benchmark GPT-4.1, GPT-4.1-mini, and GPT-4.1-nano on the same prompt.
    Print a comparison table showing:
      Model | Input Tokens | Output Tokens | Latency (ms) | Cost (USD)

    Args:
        prompt: The prompt to benchmark
    """
    models = ["gpt-4.1", "gpt-4.1-mini", "gpt-4.1-nano"]
    results = []

    print(f"Benchmarking prompt: '{prompt[:60]}...' across 3 model tiers\n")

    # TODO: For each model in models:
    #   - Call benchmark_model(model, prompt)
    #   - Append the result to results
    #   - Print progress: f"  Tested {model}"

    # TODO: Print a formatted comparison table:
    # Model          | Input Tokens | Output Tokens | Latency (ms) | Cost (USD)
    # gpt-4.1        |          ... |           ... |        ...ms |   $0.00000
    # gpt-4.1-mini   |          ... |           ... |        ...ms |   $0.00000
    # gpt-4.1-nano   |          ... |           ... |        ...ms |   $0.00000
    pass


if __name__ == "__main__":
    sample_prompt = """Analyze the following business scenario and provide a structured
    recommendation: A SaaS company has 10,000 active users and wants to add AI-powered
    features. What approach should they take to integrate LLMs cost-effectively?"""

    print("=" * 60)
    print("Exercise 1: Token Counting with tiktoken")
    print("=" * 60)
    token_count = count_tokens(sample_prompt)
    print(f"Prompt token count: {token_count} tokens")

    print("\n" + "=" * 60)
    print("Exercise 2: Cost Calculation")
    print("=" * 60)
    # Example: 100 input tokens + 200 output tokens on gpt-4.1-mini
    cost = calculate_cost("gpt-4.1-mini", 100, 200)
    print(f"Cost for 100 input + 200 output tokens on gpt-4.1-mini: ${cost:.6f}")

    print("\n" + "=" * 60)
    print("Exercise 3: Model Benchmark Comparison")
    print("=" * 60)
    run_benchmark(sample_prompt)
