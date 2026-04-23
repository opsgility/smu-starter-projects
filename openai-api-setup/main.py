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


if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: Verify Environment")
    print("=" * 50)
    # verify_environment()  # Uncomment after implementing Exercise 1

    # Uncomment when you reach Exercise 2:
    # print("\n" + "=" * 50)
    # print("Exercise 2: List GPT Models")
    # print("=" * 50)
    # list_models()

    # Uncomment when you reach Exercise 3:
    # print("\n" + "=" * 50)
    # print("Exercise 3: First Responses API Call")
    # print("=" * 50)
    # print(first_response("What are the three laws of robotics?"))

    # Uncomment when you reach Exercise 4:
    # print("\n" + "=" * 50)
    # print("Exercise 4: Inspect Response Structure")
    # print("=" * 50)
    # print(inspect_response("Explain recursion in one sentence."))
