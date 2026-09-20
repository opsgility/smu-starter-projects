"""
Vision API: Analyzing Images with GPT-4o
Course 203 - Lesson 2: Vision Exercises

Exercises:
1. Send a URL-based image to GPT-4o and describe it
2. Encode a local image as base64 and analyze it
3. Compare detail levels (low vs high) and measure token impact
4. Parse a receipt/invoice image into structured JSON

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
from pydantic import BaseModel
import base64
import json
import os

client = OpenAI()

# Sample public images for exercises
SAMPLE_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/JPEG_example_flower.jpg/800px-JPEG_example_flower.jpg"

# Sample receipt text encoded as an image (for invoice parsing exercise)
# In a real lab environment this would be an actual image file
SAMPLE_INVOICE_IMAGE_PATH = "invoice_sample.jpg"


# -----------------------------------------------------------------------
# Exercise 1: URL-based image analysis
# -----------------------------------------------------------------------

def analyze_image_url(image_url: str, question: str = "Describe this image in detail.") -> str:
    """
    Exercise 1: Send an image URL to GPT-4o and get a description.

    Use client.responses.create() with a content array containing:
    - A text part with the question
    - An image_url part with the URL

    The input should use the multi-modal content format:
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": question},
            {"type": "input_image", "image_url": image_url}
        ]
    }]

    Returns:
        The text description from response.output_text
    """
    # TODO: Call client.responses.create() with model="gpt-4o"
    # TODO: Use the multi-modal input format shown above
    # TODO: Return response.output_text
    pass


# -----------------------------------------------------------------------
# Exercise 2: Base64 image encoding and analysis
# -----------------------------------------------------------------------

def encode_image_base64(image_path: str) -> str:
    """
    Exercise 2a: Encode a local image file as base64.

    Read the image file in binary mode and encode with base64.
    Returns the base64-encoded string.
    """
    # TODO: Open image_path in "rb" mode
    # TODO: Return base64.b64encode(image_data).decode("utf-8")
    pass


def analyze_local_image(image_path: str, question: str) -> str:
    """
    Exercise 2b: Analyze a local image using base64 encoding.

    Encode the image with encode_image_base64(), then send to GPT-4o
    using the base64 image format:

    {"type": "input_image", "image_url": f"data:image/jpeg;base64,{b64_data}"}

    Returns:
        The model's text response
    """
    # TODO: Call encode_image_base64(image_path)
    # TODO: Build multi-modal input with base64 image
    # TODO: Call client.responses.create(model="gpt-4o", input=...)
    # TODO: Return response.output_text
    pass


# -----------------------------------------------------------------------
# Exercise 3: Detail levels and token impact
# -----------------------------------------------------------------------

def analyze_with_detail(image_url: str, detail: str) -> tuple[str, int]:
    """
    Exercise 3: Analyze an image with a specific detail level.

    detail parameter controls resolution: "low", "high", or "auto"

    Low detail: 85 tokens flat — fast and cheap for simple tasks
    High detail: tiles the image — higher quality, more tokens

    Use the detail parameter in the image_url content part:
    {"type": "input_image", "image_url": image_url, "detail": detail}

    Returns:
        Tuple of (response_text, total_tokens_used)
        Get total tokens from response.usage.total_tokens
    """
    # TODO: Call client.responses.create() with model="gpt-4o"
    # TODO: Include "detail": detail in the image content part
    # TODO: Return (response.output_text, response.usage.total_tokens)
    pass


def compare_detail_levels(image_url: str) -> None:
    """
    Exercise 3 driver: Compare low vs high detail and print token usage.
    """
    print("\nComparing detail levels:")
    for detail in ["low", "high"]:
        text, tokens = analyze_with_detail(image_url, detail)
        print(f"  {detail:4s} detail: {tokens:4d} tokens | Preview: {text[:60]}...")


# -----------------------------------------------------------------------
# Exercise 4: Structured invoice/receipt parsing
# -----------------------------------------------------------------------

class InvoiceItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total: float


class ParsedInvoice(BaseModel):
    vendor_name: str
    invoice_number: str
    date: str
    items: list[InvoiceItem]
    subtotal: float
    tax: float
    total_due: float


def parse_invoice_image(image_url: str) -> ParsedInvoice:
    """
    Exercise 4: Extract structured data from an invoice/receipt image.

    Use client.responses.parse() (NOT responses.create()) with:
    - model="gpt-4o"
    - Multi-modal input with the invoice image URL
    - text_format=ParsedInvoice

    System message: "You are an invoice parser. Extract all line items,
    amounts, dates, and vendor information from the invoice image."

    Returns:
        ParsedInvoice — response.output_parsed
    """
    system = "You are an invoice parser. Extract all line items, amounts, dates, and vendor information from the invoice image accurately."

    # TODO: Call client.responses.parse() with:
    #   model = "gpt-4o"
    #   input = [system message + user message with image]
    #   text_format = ParsedInvoice
    # TODO: Return response.output_parsed
    pass


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

if __name__ == "__main__":
    print("Vision API Exercises")
    print("=" * 60)

    # Exercise 1
    print("\nExercise 1: URL Image Analysis")
    description = analyze_image_url(SAMPLE_IMAGE_URL)
    if description:
        print(f"Description: {description[:200]}...")

    # Exercise 2
    print("\nExercise 2: Base64 Image Analysis")
    if os.path.exists(SAMPLE_INVOICE_IMAGE_PATH):
        result = analyze_local_image(SAMPLE_INVOICE_IMAGE_PATH, "What do you see in this image?")
        if result:
            print(f"Analysis: {result[:200]}...")
    else:
        print(f"  (Skipped — {SAMPLE_INVOICE_IMAGE_PATH} not found; use a real image path)")

    # Exercise 3
    print("\nExercise 3: Detail Level Comparison")
    compare_detail_levels(SAMPLE_IMAGE_URL)

    # Exercise 4
    print("\nExercise 4: Invoice Parsing")
    INVOICE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Invoicesample.jpg/800px-Invoicesample.jpg"
    invoice = parse_invoice_image(INVOICE_URL)
    if invoice:
        print(f"Vendor: {invoice.vendor_name}")
        print(f"Invoice #: {invoice.invoice_number}")
        print(f"Total Due: ${invoice.total_due:.2f}")
        print(f"Line items: {len(invoice.items)}")
