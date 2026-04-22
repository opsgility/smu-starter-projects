"""
Structured Responses with the OpenAI Responses API
Course 101 - Lesson 4: Structured Responses

Exercises:
1. Extract structured JSON entities using response_format json_object
2. Generate a typed FAQ item using Pydantic + client.responses.parse()
3. Handle model refusals gracefully

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
import json
from typing import Optional
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()


class FAQItem(BaseModel):
    question: str
    answer: str
    category: str
    confidence: float  # 0.0 to 1.0


def extract_json(text: str) -> dict:
    """
    TODO (Exercise 1): Extract structured entities (name, email, company) from the
    provided text. Use the Responses API with text={"format": {"type": "json_object"}}.
    Parse the returned JSON string with json.loads and return the dict.
    """
    pass


def generate_faq_item(topic: str) -> FAQItem:
    """
    TODO (Exercise 2): Use client.responses.parse(...) with text_format=FAQItem to
    generate a typed FAQItem about the given topic. Use a two-message input
    (system + user). Return response.output_parsed.
    """
    pass


def safe_generate_faq(topic: str) -> Optional[FAQItem]:
    """
    TODO (Exercise 3): Like generate_faq_item, but defensively check for refusals.
    Iterate response.output items; if any has a .refusal attribute, print it and
    return None. Also return None if response.output_parsed is None. Otherwise
    return the parsed FAQItem.
    """
    pass


if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: Extract JSON Entities")
    print("=" * 50)
    entities = extract_json(
        "Hi, I'm Alex Rivera from CloudBridge. You can reach me at alex.rivera@cloudbridge.io."
    )
    print(entities)

    print("\n" + "=" * 50)
    print("Exercise 2: Pydantic Structured Output")
    print("=" * 50)
    item = generate_faq_item("Python async/await")
    if item:
        print(f"Q: {item.question}")
        print(f"A: {item.answer}")
        print(f"Category: {item.category} | Confidence: {item.confidence:.0%}")

    print("\n" + "=" * 50)
    print("Exercise 3: Refusal Handling")
    print("=" * 50)
    result = safe_generate_faq("REST API authentication")
    print(result)
