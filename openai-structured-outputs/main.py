"""
Structured Responses with the OpenAI Responses API
Course 101 - Lesson 4: Structured Responses

Exercises:
1. Return a strictly structured JSON response using response_format
2. Parse a structured FAQ item using Pydantic + client.responses.parse()
3. Handle model refusals gracefully

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
import json

client = OpenAI()


# --- Exercise 1: JSON Schema response_format ---

def generate_product_review_json(product_name: str, rating: int) -> dict:
    """
    Exercise 1: Use response_format to enforce JSON output.

    Ask the model to generate a product review as strict JSON.
    The output must have these exact keys:
      - "product": string
      - "rating": integer (1-5)
      - "summary": string (one sentence)
      - "pros": list of 3 strings
      - "cons": list of 2 strings

    Use response_format={"type": "json_object"} in client.responses.create().
    Parse and return the JSON as a Python dict.
    """
    prompt = f"""Generate a product review for "{product_name}" with a {rating}/5 rating.
Return ONLY a JSON object with these exact keys:
- product (string)
- rating (integer 1-5)
- summary (one sentence string)
- pros (list of 3 strings)
- cons (list of 2 strings)"""

    # TODO: Call client.responses.create() with:
    #   model = "gpt-4.1-mini"
    #   input = prompt
    #   text = {"format": {"type": "json_object"}}
    # TODO: Parse response.output_text as JSON using json.loads()
    # TODO: Return the parsed dict
    pass


# --- Exercise 2: Pydantic structured output ---

class FAQItem(BaseModel):
    question: str
    answer: str
    category: str
    difficulty: str  # "beginner", "intermediate", or "advanced"


def generate_faq_item(topic: str) -> FAQItem:
    """
    Exercise 2: Use client.responses.parse() with a Pydantic model.

    Generate an FAQ item about the given topic using GPT-4.1-mini.
    The model must return a response that matches the FAQItem schema exactly.

    Use client.responses.parse() with text_format=FAQItem.
    Return response.output_parsed (which is a FAQItem instance).
    """
    prompt = f"Generate a technical FAQ item about: {topic}"

    # TODO: Call client.responses.parse() with:
    #   model = "gpt-4.1-mini"
    #   input = prompt
    #   text_format = FAQItem
    # TODO: Return response.output_parsed (type: FAQItem)
    pass


# --- Exercise 3: Handle refusals ---

class SafeResponse(BaseModel):
    content: str
    safe: bool


def safe_generate(prompt: str) -> Optional[str]:
    """
    Exercise 3: Detect and handle model refusals.

    When using client.responses.parse(), if the model refuses to answer
    (e.g., for harmful content), response.output[0].refusal will be set
    instead of output_parsed.

    Try to generate a response for the given prompt.
    If the model refuses, print a message and return None.
    If it succeeds, return response.output_parsed.content.
    """
    # TODO: Call client.responses.parse() with model="gpt-4.1-mini",
    #       input=prompt, text_format=SafeResponse
    # TODO: Check if response.output[0].refusal is not None
    #       If refused: print "Model refused: <refusal message>" and return None
    # TODO: Otherwise return response.output_parsed.content
    pass


if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: JSON Schema Response Format")
    print("=" * 50)
    review = generate_product_review_json("Wireless Noise-Canceling Headphones", 4)
    if review:
        print(json.dumps(review, indent=2))

    print("\n" + "=" * 50)
    print("Exercise 2: Pydantic Structured Output")
    print("=" * 50)
    faq = generate_faq_item("Python async/await")
    if faq:
        print(f"Q: {faq.question}")
        print(f"A: {faq.answer}")
        print(f"Category: {faq.category} | Difficulty: {faq.difficulty}")

    print("\n" + "=" * 50)
    print("Exercise 3: Refusal Handling")
    print("=" * 50)
    # Test with a benign prompt
    result = safe_generate("Explain what an API is in one sentence.")
    if result:
        print(f"Response: {result}")
