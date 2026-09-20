"""
Structured Responses with the OpenAI Responses API
Course 101 - Lesson 4: Structured Responses

Exercises:
1. Extract structured JSON entities using text={"format": {"type": "json_object"}}
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


if __name__ == "__main__":
    print("=" * 50)
    print("Exercise 1: Extract JSON Entities")
    print("=" * 50)
    # entities = extract_json(
    #     "Hi, I'm Alex Rivera from CloudBridge. You can reach me at alex.rivera@cloudbridge.io."
    # )
    # print(entities)  # Uncomment after implementing Exercise 1

    # Uncomment when you reach Exercise 2:
    # print("\n" + "=" * 50)
    # print("Exercise 2: Pydantic Structured Output")
    # print("=" * 50)
    # item = generate_faq_item("Python async/await")
    # if item:
    #     print(f"Q: {item.question}")
    #     print(f"A: {item.answer}")
    #     print(f"Category: {item.category} | Confidence: {item.confidence:.0%}")

    # Uncomment when you reach Exercise 3:
    # print("\n" + "=" * 50)
    # print("Exercise 3: Refusal Handling")
    # print("=" * 50)
    # item, err = safe_generate_faq("REST API authentication")
    # if item:
    #     print(f"OK: {item.question[:60]}")
    # else:
    #     print(f"NO RESULT: {err}")
