"""
OpenAI API Setup & First Requests
Course 101 - Lesson 2: API Setup & First Requests

Exercises:
1. Verify the OpenAI environment variables
2. List available GPT models from the OpenAI API
3. Make your first Responses API call
4. Inspect the structure of a Responses API response

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually - just create the client.
"""
import os
import openai
from openai import OpenAI

client = OpenAI()


def verify_environment() -> bool:
    """
    TODO (Exercise 1): Read OPENAI_API_KEY and OPENAI_BASE_URL from environment,
    print the first 12 chars of the key plus the base URL (or '(default)' if unset),
    print 'Environment OK', and return True. Return False if the key is missing.
    """
    pass


def list_models() -> None:
    """
    TODO (Exercise 2): Call client.models.list(), filter to models whose id starts
    with 'gpt', sort by id, and print each one on its own line. Print a header
    like 'Found {N} GPT models:' before the list.
    """
    pass


def first_response(prompt: str) -> str:
    """
    TODO (Exercise 3): Call client.responses.create(model='gpt-4.1-mini', input=prompt)
    and return response.output_text. Later in the exercise, students add a system
    message by switching input to a list of role/content dicts.
    """
    pass


def inspect_response(prompt: str) -> dict:
    """
    TODO (Exercise 4): Call the Responses API, then return a dict with these keys:
    id, model, status, output_text, input_tokens, output_tokens, total_tokens.
    Students later add a 'cost_usd' key using gpt-4.1-mini pricing
    (input $0.40/M, output $1.60/M).
    """
    pass


if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: Verify Environment")
    print("=" * 50)
    verify_environment()

    print("\n" + "=" * 50)
    print("Exercise 2: List GPT Models")
    print("=" * 50)
    list_models()

    print("\n" + "=" * 50)
    print("Exercise 3: First Responses API Call")
    print("=" * 50)
    print(first_response("What are the three laws of robotics?"))

    print("\n" + "=" * 50)
    print("Exercise 4: Inspect Response Structure")
    print("=" * 50)
    print(inspect_response("Explain recursion in one sentence."))
