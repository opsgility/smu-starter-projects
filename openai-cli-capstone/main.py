"""
Capstone Project: Command-Line AI Assistant
Course 101 - Lesson 10: Capstone Project

Build a multi-model CLI assistant that:
1. Classifies each prompt to determine task complexity
2. Routes to the appropriate model tier:
   - GPT-4.1-nano: classification / simple lookups
   - GPT-4.1-mini: general questions and summaries
   - GPT-4.1:      complex analysis, code, reasoning
3. Streams responses to the terminal
4. Logs each interaction as structured JSON
5. Handles rate limits with exponential backoff

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
import json
import time
import os
from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel
import openai
from openai import OpenAI

client = OpenAI()

LOG_FILE = "interactions.jsonl"

PRICING = {
    "gpt-4.1":      {"input": 2.00, "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
}

MODEL_MAP = {
    "simple":  "gpt-4.1-nano",
    "general": "gpt-4.1-mini",
    "complex": "gpt-4.1",
}


class ClassificationResult(BaseModel):
    complexity: Literal["simple", "general", "complex"]
    reasoning: str


def classify_prompt(prompt: str) -> ClassificationResult:
    """Classify a prompt as simple, general, or complex using gpt-4.1-nano."""


def stream_with_backoff(model: str, messages: list, max_retries: int = 3) -> tuple[str, dict]:
    """Stream a response with exponential-backoff retry on RateLimitError."""


def calculate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Compute USD cost from PRICING. See Exercise 3 in Lab 2174 for the pattern."""
    pricing = PRICING[model]
    return (input_tokens / 1_000_000) * pricing["input"] + (output_tokens / 1_000_000) * pricing["output"]


def log_interaction(entry: dict, log_file: str = LOG_FILE) -> None:
    """Append one JSON line to log_file."""


def run_cli() -> None:
    """Main CLI loop: classify each prompt, route to the right model tier, stream, and log."""


if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: Test the Classifier")
    print("=" * 50)
    # test_prompts = [  # Uncomment after implementing Exercise 1
    #     "What is 7 times 8?",
    #     "Explain how Docker containers work",
    #     "Review this Python function for bugs: def add(a,b): return a - b",
    # ]
    # for p in test_prompts:
    #     r = classify_prompt(p)
    #     print(f"[{r.complexity} -> {MODEL_MAP[r.complexity]}]  {p[:60]}")
    #     print(f"  reasoning: {r.reasoning[:80]}")

    # Uncomment when you reach Exercise 2:
    # print("\n" + "=" * 50)
    # print("Exercise 2: Test Streaming with Backoff")
    # print("=" * 50)
    # messages = [
    #     {"role": "system", "content": "You are a concise technical assistant."},
    #     {"role": "user", "content": "What are the benefits of async Python?"},
    # ]
    # text, usage = stream_with_backoff("gpt-4.1-mini", messages)
    # print(f"\nTokens: {usage}")

    # Uncomment when you reach Exercise 3:
    # print("\n" + "=" * 50)
    # print("Exercise 3: Run the Full CLI Assistant")
    # print("=" * 50)
    # run_cli()
