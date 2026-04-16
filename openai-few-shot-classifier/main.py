"""
Few-Shot Ticket Classifier
Course 102 - Lesson 4: Ticket Classifier with Few-Shot Examples

Exercises:
1. Build a support ticket classifier using few-shot prompting
2. Return classification results as structured JSON
3. Measure classifier accuracy on a test set

Categories: "engineering", "billing", "sales"

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
from pydantic import BaseModel
import json

client = OpenAI()

# Few-shot examples for the classifier
# These examples guide the model without fine-tuning
FEW_SHOT_EXAMPLES = [
    {"ticket": "The API is returning 500 errors on the /users endpoint since the last deploy.", "category": "engineering"},
    {"ticket": "Why was I charged twice for my subscription this month?", "category": "billing"},
    {"ticket": "We're a team of 50 and want to discuss enterprise pricing options.", "category": "sales"},
    {"ticket": "Our webhook is not triggering after a successful payment.", "category": "engineering"},
    {"ticket": "I need a refund for the annual plan I purchased yesterday.", "category": "billing"},
    {"ticket": "Can you tell me about the differences between your Pro and Business plans?", "category": "sales"},
]

# Test set with ground truth labels
TEST_TICKETS = [
    {"ticket": "The dashboard is completely blank when I log in from Chrome.", "expected": "engineering"},
    {"ticket": "I was charged $99 but should have been charged $49.", "expected": "billing"},
    {"ticket": "We want to buy 500 seats for our company.", "expected": "sales"},
    {"ticket": "The Python SDK is throwing an ImportError on version 2.1.0.", "expected": "engineering"},
    {"ticket": "My credit card expired. How do I update it?", "expected": "billing"},
    {"ticket": "Do you offer a nonprofit discount?", "expected": "sales"},
    {"ticket": "Our CI/CD pipeline fails when running your test suite.", "expected": "engineering"},
    {"ticket": "I need an invoice for my February subscription payment.", "expected": "billing"},
    {"ticket": "Can we schedule a demo for next week?", "expected": "sales"},
    {"ticket": "The mobile app crashes when uploading files larger than 10MB.", "expected": "engineering"},
]


class ClassificationResult(BaseModel):
    category: str        # "engineering", "billing", or "sales"
    confidence: str      # "high", "medium", or "low"
    reasoning: str       # One sentence explaining why


def build_few_shot_prompt(ticket: str) -> list[dict]:
    """
    Exercise 1: Build a few-shot prompt using the FEW_SHOT_EXAMPLES list.

    Construct an input list for the Responses API that includes:
    1. A system message explaining the task and categories
    2. Alternating user/assistant messages for each few-shot example
       user:      {"ticket": "...", "text": "..."}   (show just the ticket text)
       assistant: {"category": "...", "confidence": "high", "reasoning": "..."}
    3. A final user message with the ticket to classify

    The system message should:
    - Define the three categories
    - Instruct the model to respond ONLY with valid JSON matching ClassificationResult

    Args:
        ticket: The support ticket text to classify

    Returns:
        A list of message dicts for use in client.responses.create(input=...)
    """
    messages = []

    # TODO: Add system message defining categories and JSON format
    messages.append({
        "role": "system",
        "content": """You are a support ticket classifier. Classify each ticket into exactly one category:
- "engineering": bugs, technical issues, API problems, SDK errors, deployment issues
- "billing": charges, refunds, invoices, payment methods, subscription issues
- "sales": pricing, demos, enterprise plans, account upgrades, partnerships

Respond ONLY with valid JSON matching this schema:
{"category": "engineering|billing|sales", "confidence": "high|medium|low", "reasoning": "one sentence"}"""
    })

    # TODO: Add few-shot example pairs from FEW_SHOT_EXAMPLES
    # For each example, add:
    #   {"role": "user",      "content": example["ticket"]}
    #   {"role": "assistant", "content": json.dumps({"category": example["category"], "confidence": "high", "reasoning": "..."})}
    for example in FEW_SHOT_EXAMPLES:
        # TODO: Add user message with example ticket
        # TODO: Add assistant message with JSON classification
        pass

    # TODO: Add the final user message with the ticket to classify
    messages.append({"role": "user", "content": ticket})

    return messages


def classify_ticket(ticket: str) -> ClassificationResult:
    """
    Exercise 2: Classify a support ticket using few-shot prompting.

    Use build_few_shot_prompt() to construct the input.
    Use client.responses.parse() with text_format=ClassificationResult.
    Return response.output_parsed.

    Args:
        ticket: The support ticket text

    Returns:
        ClassificationResult with category, confidence, and reasoning
    """
    messages = build_few_shot_prompt(ticket)

    # TODO: Call client.responses.parse() with:
    #   model = "gpt-4.1-mini"
    #   input = messages
    #   text_format = ClassificationResult
    # TODO: Return response.output_parsed
    pass


def evaluate_classifier() -> float:
    """
    Exercise 3: Evaluate the classifier accuracy on TEST_TICKETS.

    For each test ticket:
    - Call classify_ticket()
    - Compare result.category with the expected category
    - Track correct and total counts

    Print a table showing each ticket, prediction, expected, and PASS/FAIL.
    Print the final accuracy percentage.
    Return the accuracy as a float (0.0 to 1.0).

    Target: >= 85% accuracy (8.5/10 or better on the test set)
    """
    correct = 0
    total = len(TEST_TICKETS)

    print(f"{'Ticket (truncated)':<50} {'Expected':<12} {'Predicted':<12} {'Match'}")
    print("-" * 90)

    for item in TEST_TICKETS:
        # TODO: Call classify_ticket(item["ticket"])
        # TODO: Compare result.category with item["expected"]
        # TODO: Increment correct if they match
        # TODO: Print the table row
        pass

    accuracy = correct / total
    print(f"\nAccuracy: {correct}/{total} = {accuracy:.1%}")
    print(f"Target: >= 85% {'✓ PASS' if accuracy >= 0.85 else '✗ FAIL'}")
    return accuracy


if __name__ == "__main__":
    print("=" * 60)
    print("Exercise 1 & 2: Few-Shot Ticket Classification")
    print("=" * 60)
    sample = "The export to CSV feature is broken - it downloads an empty file."
    result = classify_ticket(sample)
    if result:
        print(f"Ticket: {sample}")
        print(f"Category: {result.category}")
        print(f"Confidence: {result.confidence}")
        print(f"Reasoning: {result.reasoning}")

    print("\n" + "=" * 60)
    print("Exercise 3: Classifier Accuracy Evaluation")
    print("=" * 60)
    evaluate_classifier()
