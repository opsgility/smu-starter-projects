"""
Structured Outputs with Pydantic - Data Extraction Pipeline
Course 201 - Lesson 6: Data Extraction Pipeline

Exercise 1: Extract structured contact information from unstructured email text
Exercise 2: Extract invoice line items from invoice text into typed Pydantic models

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
from pydantic import BaseModel, Field
from typing import Optional
import json

client = OpenAI()

# -----------------------------------------------------------------------
# Sample unstructured data for extraction
# -----------------------------------------------------------------------

SAMPLE_EMAILS = [
    """Hi, I'm Sarah Johnson from Acme Corp. You can reach me at sarah.johnson@acme.com
    or call me at (555) 867-5309. Our office is at 742 Evergreen Terrace, Springfield, IL 62701.
    I'm the VP of Engineering and wanted to discuss our enterprise subscription.""",

    """Hello team, this is Dr. Michael Chen. My contact info: m.chen@medcore.io,
    phone +1-415-555-0142. I'm based in San Francisco, CA. As the CTO of MedCore Systems,
    I'm interested in the API plan. Please send pricing to my assistant at
    assistant@medcore.io as well.""",

    """Reaching out from RetailMax. I'm Jamie Torres, Sales Director. Best email is
    jtorres@retailmax.com, mobile 312.555.7788. Address: 1000 N. Michigan Ave, Chicago IL 60611.
    Looking for a demo ASAP!""",
]

SAMPLE_INVOICES = [
    """INVOICE #2026-001
    Vendor: CloudStack Solutions | Date: April 1, 2026
    Bill To: DevOps Inc.

    Cloud hosting (March 2026): $1,200.00
    Database managed service (3 months @ $300/month): $900.00
    SSL certificate (annual): $149.00
    Support package - Business tier: $299.00
    Setup fee (one-time): $500.00

    Subtotal: $3,048.00
    Tax (8%): $243.84
    TOTAL: $3,291.84
    Payment due: May 1, 2026""",

    """Invoice from DataFlow Analytics
    Invoice Number: DF-2026-0892 | Issued: March 15, 2026

    To: FinTech Startup Ltd.

    1. Data pipeline setup - 40 hours @ $125/hr = $5,000.00
    2. Monthly SaaS subscription (2 months): $800.00
    3. Custom dashboard development: $2,500.00
    4. Training session (4 hours @ $200/hr): $800.00

    Total before tax: $9,100.00
    Sales tax 9.5%: $864.50
    Amount due: $9,964.50 | Due: April 15, 2026""",
]


# -----------------------------------------------------------------------
# Exercise 1: Contact Information Extraction
# -----------------------------------------------------------------------

class ContactInfo(BaseModel):
    full_name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None
    address: Optional[str] = None
    additional_emails: list[str] = Field(default_factory=list)


def extract_contact_info(email_text: str) -> ContactInfo:
    """
    Exercise 1: Extract structured contact information from an unstructured email.

    Use client.responses.parse() with text_format=ContactInfo.
    The model must extract all contact fields from the free-form text.

    Handle the case where a field is not mentioned (use None or empty list).
    Verify response.output_parsed is a valid ContactInfo before returning.

    Args:
        email_text: Unstructured email text containing contact information

    Returns:
        ContactInfo with all extracted fields
    """
    prompt = f"""Extract contact information from this email.
If a field is not mentioned, leave it as null or empty.

Email:
{email_text}"""

    # TODO: Call client.responses.parse() with:
    #   model = "gpt-4.1-mini"
    #   input = prompt
    #   text_format = ContactInfo
    # TODO: Check if response.output[0].refusal is not None -> raise ValueError
    # TODO: Return response.output_parsed
    pass


# -----------------------------------------------------------------------
# Exercise 2: Invoice Line Item Extraction
# -----------------------------------------------------------------------

class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = 1.0
    unit_price: Optional[float] = None
    total: float
    item_type: str  # "service", "product", "subscription", "fee", "other"


class Invoice(BaseModel):
    invoice_number: str
    vendor_name: str
    client_name: str
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    line_items: list[LineItem]
    subtotal: float
    tax_amount: Optional[float] = None
    tax_rate_pct: Optional[float] = None
    total: float
    currency: str = "USD"


def extract_invoice(invoice_text: str) -> Invoice:
    """
    Exercise 2: Extract a complete invoice with line items from unstructured text.

    Use client.responses.parse() with text_format=Invoice.
    The model must identify all line items with their prices and types.

    strict=True in Pydantic means all required fields must be populated.
    Pay attention to the Invoice schema: every LineItem needs description and total.

    Args:
        invoice_text: Unstructured invoice text

    Returns:
        Invoice with all line items and totals
    """
    prompt = f"""Extract all invoice data from this text into structured format.
Extract every line item with its description, quantity, unit price, total, and type.
Item types: service, product, subscription, fee, other.

Invoice text:
{invoice_text}"""

    # TODO: Call client.responses.parse() with:
    #   model = "gpt-4.1"
    #   input = prompt
    #   text_format = Invoice
    # TODO: Handle refusal case
    # TODO: Return response.output_parsed
    pass


def validate_invoice_totals(invoice: Invoice) -> bool:
    """
    Bonus: Validate that line items sum to the reported subtotal.
    Returns True if within $0.05 tolerance, False otherwise.
    """
    if not invoice or not invoice.line_items:
        return False
    calculated = sum(item.total for item in invoice.line_items)
    return abs(calculated - invoice.subtotal) < 0.05


if __name__ == "__main__":
    print("=" * 60)
    print("Exercise 1: Contact Information Extraction")
    print("=" * 60)

    for i, email in enumerate(SAMPLE_EMAILS, 1):
        print(f"\nEmail {i}:")
        print(f"  Text: {email[:80]}...")
        contact = extract_contact_info(email)
        if contact:
            print(f"  Name:    {contact.full_name}")
            print(f"  Email:   {contact.email}")
            print(f"  Phone:   {contact.phone}")
            print(f"  Company: {contact.company}")
            print(f"  Title:   {contact.job_title}")

    print("\n" + "=" * 60)
    print("Exercise 2: Invoice Line Item Extraction")
    print("=" * 60)

    for i, invoice_text in enumerate(SAMPLE_INVOICES, 1):
        print(f"\nInvoice {i}:")
        invoice = extract_invoice(invoice_text)
        if invoice:
            print(f"  #{invoice.invoice_number} from {invoice.vendor_name}")
            print(f"  {len(invoice.line_items)} line items | Total: ${invoice.total:,.2f}")
            for item in invoice.line_items:
                print(f"    • {item.description[:50]}: ${item.total:,.2f} ({item.item_type})")
            validation = validate_invoice_totals(invoice)
            print(f"  Totals validate: {'✓' if validation else '✗'}")
