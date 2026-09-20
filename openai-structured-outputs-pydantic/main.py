"""
Data Extraction Pipeline
Course 201 - Lesson 6: Structured Outputs with Pydantic

Extract structured data from unstructured text using Pydantic models
and the Responses API structured output feature.

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
import json

client = OpenAI()


# -----------------------------------------------------------------------
# Exercise 1: Contact Information Extraction
# -----------------------------------------------------------------------

class ContactInfo(BaseModel):
    name: str
    email: Optional[str]
    phone: Optional[str]
    company: Optional[str]
    role: Optional[str]


SAMPLE_EMAILS = [
    """Hi, I'm Sarah Chen, Senior Engineer at TechFlow Inc.
    You can reach me at sarah.chen@techflow.io or call 415-555-0199.
    Looking forward to connecting!""",

    """From: James Park <james.park@medcore.com>
    I'm the CFO at MedCore Systems. My direct line is (512) 555-7823.
    Please cc billing@medcore.com on all invoices.""",

    """Hello! Rachel Torres here. I don't have a company email yet but
    you can reach me at rachel.torres.personal@gmail.com. No phone for now.""",
]


def extract_contact(email_text: str) -> ContactInfo:
    """
    Exercise 1: Extract contact information from an email.

    Use client.responses.parse() with:
    - model="gpt-4.1-mini"
    - input=[system message, user message with email text]
    - text_format=ContactInfo

    System prompt: "Extract contact information from emails. Return null
    for any fields not present in the text."

    Returns:
        ContactInfo with extracted fields (None for missing data)
    """
    system = "Extract contact information from emails. Return null for any fields not present in the text."

    # TODO: Call client.responses.parse() with ContactInfo schema
    # TODO: Check if response.output_parsed is None (refusal)
    # TODO: Return response.output_parsed
    pass


# -----------------------------------------------------------------------
# Exercise 2: Invoice Line Item Extraction
# -----------------------------------------------------------------------

class LineItem(BaseModel):
    description: str
    quantity: int
    unit_price: float
    total: float


class InvoiceData(BaseModel):
    invoice_number: str
    vendor: str
    customer: str
    invoice_date: str
    due_date: str
    line_items: list[LineItem]
    subtotal: float
    tax: float
    total_due: float


SAMPLE_INVOICE = """INVOICE #INV-2026-0342

From: TechFlow Solutions Inc., 123 Market Street, San Francisco, CA 94105
To:   ShopMax Retail Group, 456 Commerce Blvd, Austin, TX 78701

Invoice Date: March 1, 2026
Due Date: March 31, 2026

SERVICES:
AI Analytics Platform License (February 2026)    1 unit @ $8,500.00    $8,500.00
Custom Dashboard Development                    15 hours @ $200.00    $3,000.00
Priority Support Package                         1 unit @ $1,500.00    $1,500.00

Subtotal:   $13,000.00
Tax (8.5%):  $1,105.00
TOTAL DUE:  $14,105.00
"""


def extract_invoice(invoice_text: str) -> InvoiceData:
    """
    Exercise 2: Extract all line items and totals from an invoice.

    Use client.responses.parse() with:
    - model="gpt-4.1"
    - input=[system message, user message with invoice text]
    - text_format=InvoiceData

    System prompt: "Extract invoice data exactly as written. Do not
    calculate or infer values — extract only what is present in the text."

    Returns:
        InvoiceData with all fields populated
    """
    system = "Extract invoice data exactly as written. Do not calculate or infer values — extract only what is present in the text."

    # TODO: Call client.responses.parse() with InvoiceData schema
    # TODO: Handle refusal case
    # TODO: Return response.output_parsed
    pass


# -----------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------

if __name__ == "__main__":
    print("Data Extraction Pipeline — Course 201 Lesson 6")
    print("=" * 50)

    # Exercise 1: Contact extraction
    print("\n--- Exercise 1: Contact Extraction ---")
    for i, email in enumerate(SAMPLE_EMAILS, 1):
        contact = extract_contact(email)
        if contact:
            print(f"\nEmail {i}:")
            print(f"  Name:    {contact.name}")
            print(f"  Email:   {contact.email or 'N/A'}")
            print(f"  Phone:   {contact.phone or 'N/A'}")
            print(f"  Company: {contact.company or 'N/A'}")
            print(f"  Role:    {contact.role or 'N/A'}")

    # Exercise 2: Invoice extraction
    print("\n--- Exercise 2: Invoice Extraction ---")
    invoice = extract_invoice(SAMPLE_INVOICE)
    if invoice:
        print(f"\nInvoice:  {invoice.invoice_number}")
        print(f"Vendor:   {invoice.vendor}")
        print(f"Customer: {invoice.customer}")
        print(f"Due:      {invoice.due_date}")
        print(f"\nLine Items ({len(invoice.line_items)}):")
        for item in invoice.line_items:
            print(f"  {item.description:<45} ${item.total:>10.2f}")
        print(f"\n  Subtotal: ${invoice.subtotal:>10.2f}")
        print(f"  Tax:      ${invoice.tax:>10.2f}")
        print(f"  TOTAL:    ${invoice.total_due:>10.2f}")
