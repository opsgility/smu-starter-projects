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
from openai import OpenAI
import tiktoken
import time
import json
import os
from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel

client = OpenAI()

# Log file for structured interaction logging
LOG_FILE = "interaction_log.jsonl"

# Model routing tiers
ModelTier = Literal["gpt-4.1-nano", "gpt-4.1-mini", "gpt-4.1"]

# Pricing per 1M tokens
PRICING = {
    "gpt-4.1":      {"input": 2.00,  "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40,  "output": 1.60},
    "gpt-4.1-nano": {"input": 0.10,  "output": 0.40},
}


class ClassificationResult(BaseModel):
    complexity: Literal["simple", "general", "complex"]
    reasoning: str


def classify_prompt(prompt: str) -> ModelTier:
    """
    Exercise 1: Classify prompt complexity and select the appropriate model.

    Use GPT-4.1-nano with client.responses.parse() to classify the prompt as:
    - "simple":  single-fact lookups, yes/no questions, short classification
    - "general": summaries, explanations, conversational questions
    - "complex": code generation, analysis, multi-step reasoning, technical depth

    Map classification to model tier:
    - simple  -> gpt-4.1-nano
    - general -> gpt-4.1-mini
    - complex -> gpt-4.1

    Returns the model name string.
    """
    classification_prompt = f"""Classify the following user prompt by complexity:
- simple: single-fact lookup, yes/no, short answer
- general: explanation, summary, conversational
- complex: code generation, deep analysis, multi-step reasoning

Prompt: "{prompt}"
"""
    # TODO: Call client.responses.parse() with model="gpt-4.1-nano",
    #       input=classification_prompt, text_format=ClassificationResult
    # TODO: Map result.output_parsed.complexity to the correct model tier
    # TODO: Return the model name string
    return "gpt-4.1-mini"  # Default - replace with your implementation


def call_with_backoff(model: str, prompt: str, max_retries: int = 3) -> object:
    """
    Exercise 2: Make an API call with exponential backoff on rate limit errors.

    Attempt client.responses.create() up to max_retries times.
    On openai.RateLimitError, wait 2^attempt seconds before retrying.
    Print a message when retrying: "Rate limited. Retrying in Xs..."
    Raise the error if all retries are exhausted.

    Returns the response object.
    """
    import openai

    for attempt in range(max_retries):
        # TODO: Try client.responses.create(model=model, input=prompt, stream=False)
        # TODO: On openai.RateLimitError: calculate wait = 2 ** attempt
        #       print(f"Rate limited. Retrying in {wait}s..."), time.sleep(wait)
        # TODO: On final attempt, re-raise the exception
        pass


def stream_response(model: str, prompt: str) -> tuple[str, int, int]:
    """
    Exercise 3: Stream the response and return (text, input_tokens, output_tokens).

    Use client.responses.stream() to stream the response.
    Print each text delta as it arrives (end="", flush=True).
    After streaming completes, get usage from stream.get_final_response().usage.
    Return the assembled text and token counts.
    """
    full_text = ""
    input_tokens = 0
    output_tokens = 0

    # TODO: Use 'with client.responses.stream(model=model, input=prompt) as stream:'
    # TODO: Iterate over stream.text_stream, print each delta, append to full_text
    # TODO: After the with block: final = stream.get_final_response()
    # TODO: input_tokens = final.usage.input_tokens
    # TODO: output_tokens = final.usage.output_tokens
    # TODO: Return (full_text, input_tokens, output_tokens)

    return full_text, input_tokens, output_tokens


def log_interaction(prompt: str, model: str, output: str,
                    input_tokens: int, output_tokens: int,
                    latency_ms: float) -> None:
    """
    Exercise 4: Log each interaction as a JSON record in interaction_log.jsonl.

    Each log entry must include:
      - timestamp (ISO 8601 UTC)
      - model
      - input_tokens
      - output_tokens
      - cost_usd (calculate from PRICING)
      - latency_ms
      - prompt (first 200 chars)
      - output (first 200 chars)

    Append the JSON record (one per line) to LOG_FILE.
    """
    # TODO: Calculate cost_usd using PRICING dict
    # TODO: Build log_entry dict with all required fields
    # TODO: Append json.dumps(log_entry) + "\n" to LOG_FILE
    pass


def run_assistant() -> None:
    """
    Exercise 5: The main interactive loop.

    Loop until the user types 'quit' or 'exit'.
    For each prompt:
    1. Classify -> select model
    2. Print which model was selected and why
    3. Stream the response (with backoff)
    4. Log the interaction
    5. Print token usage and cost for this interaction
    """
    print("Multi-Model CLI Assistant")
    print("Type 'quit' to exit | 'log' to view last 3 interactions\n")

    while True:
        try:
            prompt = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not prompt:
            continue
        if prompt.lower() in ("quit", "exit"):
            print("Goodbye!")
            break
        if prompt.lower() == "log":
            # TODO: Read and print last 3 lines from LOG_FILE
            # Each line is a JSON object - print it formatted
            continue

        # TODO: Record start time
        start = time.time()

        # TODO: Step 1 - Classify the prompt
        model = classify_prompt(prompt)
        print(f"\n[Routing to {model}]\n")

        # TODO: Step 2 - Stream the response with backoff
        print("Assistant: ", end="", flush=True)
        # ... call stream_response or call_with_backoff + stream ...

        # TODO: Step 3 - Log the interaction

        # TODO: Step 4 - Print usage summary
        # latency_ms = (time.time() - start) * 1000
        # print(f"\n[{model} | {input_tokens} in / {output_tokens} out | ${cost:.6f} | {latency_ms:.0f}ms]")
        print()


if __name__ == "__main__":
    run_assistant()
