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
    """
    TODO (Exercise 1): Use client.responses.parse with a classifier system prompt
    and text_format=ClassificationResult. Return response.output_parsed. If parsing
    fails, return ClassificationResult(complexity='general', reasoning='fallback').
    """
    pass


def stream_with_backoff(model: str, messages: list, max_retries: int = 3) -> tuple[str, dict]:
    """
    TODO (Exercise 2): Stream a response with client.responses.stream(model=model,
    input=messages). Iterate events with `for event in stream` and print
    event.delta when event.type == "response.output_text.delta". Catch
    openai.RateLimitError and retry with exponential backoff (sleep 2 ** attempt
    seconds) up to max_retries times. Return (full_text, usage_dict) where
    usage_dict has keys input_tokens, output_tokens, total_tokens.
    """
    pass


def calculate_cost(input_tokens: int, output_tokens: int, model: str) -> float:
    """Compute USD cost from PRICING. See Exercise 3 in Lab 2174 for the pattern."""
    pricing = PRICING[model]
    return (input_tokens / 1_000_000) * pricing["input"] + (output_tokens / 1_000_000) * pricing["output"]


def log_interaction(entry: dict, log_file: str = LOG_FILE) -> None:
    """
    TODO (Exercise 3): Append one JSON line to log_file. The entry dict should
    already contain: timestamp, prompt_preview, complexity, model_used,
    input_tokens, output_tokens, cost_usd, latency_seconds.
    """
    pass


def run_cli() -> None:
    """
    TODO (Exercise 3): Main CLI loop. Read user prompts with input(); exit on
    empty/quit/exit. For each prompt:
      1. classification = classify_prompt(prompt)
      2. model = MODEL_MAP[classification.complexity]
      3. Time stream_with_backoff(model, [{'role':'user','content':prompt}])
      4. Print response as it streams (already printed inside stream_with_backoff)
      5. Build entry dict with all 8 fields above and call log_interaction(entry)
      6. Print a one-line footer:
         f"[{usage['total_tokens']} tokens | ${cost:.6f} | {latency:.2f}s]"
    """
    pass


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
