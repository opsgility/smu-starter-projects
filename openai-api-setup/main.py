"""
OpenAI API Setup & First Requests
Course 101 - Lesson 2: API Setup & First Requests

Exercises:
1. List available models from the OpenAI API
2. Make your first Responses API call using GPT-4.1-mini
3. Validate the response structure (output_text, model name, usage)

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually - just create the client.
"""
from openai import OpenAI

# Initialize the OpenAI client
# The API key and base URL are injected into your environment automatically
client = OpenAI()


def list_available_models():
    """
    Exercise 1: List available models from the OpenAI API.

    Use client.models.list() to retrieve all models available to your account.
    Print each model's .id property, sorted alphabetically.
    """
    # TODO: Call client.models.list() to get all models
    # TODO: Sort the models by their .id attribute
    # TODO: Print each model ID on its own line
    # Expected output: A sorted list of model IDs (gpt-4.1, gpt-4.1-mini, etc.)
    pass


def make_first_request():
    """
    Exercise 2: Make your first call using the OpenAI Responses API.

    The Responses API is the modern alternative to Chat Completions.
    Use client.responses.create() with model="gpt-4.1-mini".
    Access the text result via response.output_text.
    """
    prompt = "Introduce yourself in exactly two sentences. Mention that you are GPT-4.1-mini."

    # TODO: Call client.responses.create() with:
    #   model = "gpt-4.1-mini"
    #   input = prompt
    # TODO: Print response.output_text to display the result
    pass


def validate_response_structure():
    """
    Exercise 3: Inspect the full response object.

    Make a Responses API call and examine its structure:
    - response.model        -> the model that processed the request
    - response.output_text  -> the text output
    - response.usage        -> token counts (input_tokens, output_tokens)

    Print a summary showing each of these values.
    """
    prompt = "What is the capital of France? Answer in one word."

    # TODO: Call client.responses.create() with model="gpt-4.1-mini"
    # TODO: Capture the full response object
    # TODO: Print response.model
    # TODO: Print response.output_text
    # TODO: Print response.usage.input_tokens and response.usage.output_tokens
    pass


if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: List Available Models")
    print("=" * 50)
    list_available_models()

    print("\n" + "=" * 50)
    print("Exercise 2: First Responses API Call")
    print("=" * 50)
    make_first_request()

    print("\n" + "=" * 50)
    print("Exercise 3: Validate Response Structure")
    print("=" * 50)
    validate_response_structure()
