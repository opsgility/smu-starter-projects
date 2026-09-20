"""
Capstone Project: Intelligent Document Processor
Course 102 - Lesson 10: Capstone Project

Build a document processing pipeline that:
Stage 1: Extract named entities and dates (few-shot prompting)
Stage 2: Classify document type (contract, invoice, report) with CoT
Stage 3: Generate executive summary (persona-based system prompt)
+ Prompt injection guard on all user-supplied input
+ Cost report: tokens and estimated USD per document processed

Sample documents are provided in the DOCUMENTS dict below.
The pipeline should handle all three document types correctly.

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional, Literal
import json
import re
import time
from datetime import datetime, timezone

client = OpenAI()

PRICING = {
    "gpt-4.1":      {"input": 2.00,  "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40,  "output": 1.60},
}

# Sample documents for testing - one of each type
DOCUMENTS = {
    "contract": """SERVICE AGREEMENT

This Service Agreement ("Agreement") is entered into as of January 15, 2026, between
TechFlow Solutions Inc., a Delaware corporation ("Service Provider"), and MedCore Systems LLC,
a California limited liability company ("Client").

1. SERVICES. Service Provider agrees to provide AI-powered analytics platform services
   beginning February 1, 2026 through January 31, 2027.

2. PAYMENT TERMS. Client shall pay $12,500 per month, due on the first day of each month.
   Late payments incur a 1.5% monthly interest charge.

3. CONFIDENTIALITY. Both parties agree to maintain strict confidentiality of all proprietary
   information shared during the term of this Agreement.

4. TERMINATION. Either party may terminate with 30 days written notice to Sarah Chen, CEO
   at TechFlow Solutions or Rachel Torres, CFO at MedCore Systems.

Signed: Sarah Chen (TechFlow Solutions) and James Park (MedCore Systems) on January 15, 2026.
""",

    "invoice": """INVOICE #INV-2026-0342

From: TechFlow Solutions Inc., 123 Market Street, San Francisco, CA 94105
To:   ShopMax Retail Group, 456 Commerce Blvd, Austin, TX 78701

Invoice Date: March 1, 2026
Due Date: March 31, 2026

SERVICES:
AI Analytics Platform License (February 2026)    $8,500.00
Custom Dashboard Development (15 hours @ $200)   $3,000.00
Priority Support Package                         $1,500.00
                                                ----------
Subtotal:                                       $13,000.00
Tax (8.5%):                                      $1,105.00
                                                ----------
TOTAL DUE:                                      $14,105.00

Payment Methods: Wire transfer, ACH, or check payable to TechFlow Solutions Inc.
Questions? Contact billing@techflow.io or call 415-555-0199.
""",

    "report": """Q1 2026 PERFORMANCE REPORT
TechFlow Solutions Inc. — Confidential

Prepared by: Rachel Torres, CFO | Date: April 5, 2026

EXECUTIVE SUMMARY
Q1 2026 marked a breakthrough quarter for TechFlow, with revenue reaching $3.2M,
representing 67% year-over-year growth. Net new ARR of $1.8M exceeded our $1.5M target.

KEY METRICS
- Monthly Recurring Revenue: $1.067M (up from $725K in Q1 2025)
- Customer Count: 1,847 (added 312 net new customers)
- Average Contract Value: $6,820 (up 23%)
- Churn Rate: 1.2% (improved from 2.1%)
- Employee Count: 143 (hired 28 in Q1)

HIGHLIGHTS
- Closed 3 enterprise deals > $500K ARR including GlobalBank and RetailMax
- Launched AI Insights Pro tier generating $420K in upgrade revenue
- Engineering team reduced API latency by 40% (from 250ms to 150ms p95)

OUTLOOK
Q2 2026 pipeline is $8.4M, with $2.1M in advanced stages.
We expect to exceed $4M quarterly revenue by Q2 and reach profitability by Q4 2026.
"""
}


class ExtractedEntities(BaseModel):
    people: list[str]
    organizations: list[str]
    dates: list[str]
    monetary_amounts: list[str]
    key_terms: list[str]


class DocumentClassification(BaseModel):
    document_type: Literal["contract", "invoice", "report"]
    confidence: float
    reasoning: str
    chain_of_thought: str


class DocumentSummary(BaseModel):
    title: str
    key_points: list[str]
    financial_highlights: list[str]
    action_required: str
    risk_flags: list[str]


class ProcessingCost(BaseModel):
    stage: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


# Injection detection
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|above|prior)\s+instructions?",
    r"forget\s+(your|all)\s+(instructions?|prompt|rules?)",
    r"jailbreak|DAN\s+mode",
    r"system\s+prompt\s*(override|bypass)",
    r"<\s*system\s*>",
]


def check_injection(text: str) -> bool:
    """Return True if injection detected, False if safe."""
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    p = PRICING.get(model, {"input": 0, "output": 0})
    return (input_tokens / 1_000_000) * p["input"] + (output_tokens / 1_000_000) * p["output"]


def stage1_extract_entities(document: str) -> tuple[ExtractedEntities, ProcessingCost]:
    """
    Stage 1: Extract entities using few-shot prompting.

    Build a few-shot prompt with 2-3 examples showing entity extraction.
    Use client.responses.parse() with ExtractedEntities schema.
    Return (entities, cost_record).
    """
    few_shot_prompt = """Extract named entities from documents. Examples:

Document: "Contract signed by John Smith (Acme Corp) and Jane Doe (Beta Inc) on Jan 1, 2026 for $10,000."
Result: {"people": ["John Smith", "Jane Doe"], "organizations": ["Acme Corp", "Beta Inc"], "dates": ["January 1, 2026"], "monetary_amounts": ["$10,000"], "key_terms": ["Contract"]}

Document: "Invoice #001 from TechCo to RetailMax. Amount due: $5,500. Due March 15, 2026."
Result: {"people": [], "organizations": ["TechCo", "RetailMax"], "dates": ["March 15, 2026"], "monetary_amounts": ["$5,500"], "key_terms": ["Invoice"]}

Now extract from this document:
""" + document

    # TODO: Call client.responses.parse() with model="gpt-4.1-mini",
    #       input=few_shot_prompt, text_format=ExtractedEntities
    # TODO: Create ProcessingCost using response.usage tokens
    # TODO: Return (response.output_parsed, cost_record)
    pass


def stage2_classify_document(document: str, entities: ExtractedEntities) -> tuple[DocumentClassification, ProcessingCost]:
    """
    Stage 2: Classify document type using chain-of-thought reasoning.

    Prompt the model to think step-by-step before classifying:
    1. What type of language does it use?
    2. What entities are present?
    3. What is the primary purpose?
    Then classify as: contract, invoice, or report.

    Use client.responses.parse() with DocumentClassification schema.
    Return (classification, cost_record).
    """
    cot_prompt = f"""Classify this document as: contract, invoice, or report.

Think step by step:
1. Analyze the document language and structure
2. Consider the entities: people={entities.people}, orgs={entities.organizations}
3. Identify the primary purpose (legal agreement / financial billing / performance data)
4. Determine document type with confidence (0.0-1.0)

Document:
{document}"""

    # TODO: Call client.responses.parse() with model="gpt-4.1-mini",
    #       input=cot_prompt, text_format=DocumentClassification
    # TODO: Create ProcessingCost from usage
    # TODO: Return (response.output_parsed, cost_record)
    pass


def stage3_generate_summary(document: str, doc_type: str,
                             entities: ExtractedEntities) -> tuple[DocumentSummary, ProcessingCost]:
    """
    Stage 3: Generate executive summary using persona-based system prompt.

    System prompt persona: "You are a senior legal and financial analyst reviewing
    documents for executive briefings. Be concise, flag risks, and highlight
    anything requiring immediate action."

    Use client.responses.parse() with DocumentSummary schema.
    Return (summary, cost_record).
    """
    system = """You are a senior legal and financial analyst reviewing documents for executive briefings.
Be concise, flag risks, and highlight anything requiring immediate action.
Focus on: financial exposure, key parties, deadlines, and compliance issues."""

    user = f"""Create an executive summary for this {doc_type}.

Document:
{document}

Key entities identified: people={entities.people}, monetary={entities.monetary_amounts}, dates={entities.dates}"""

    # TODO: Call client.responses.parse() with:
    #   model = "gpt-4.1"
    #   input = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    #   text_format = DocumentSummary
    # TODO: Create ProcessingCost from usage
    # TODO: Return (response.output_parsed, cost_record)
    pass


def process_document(document_text: str, document_name: str) -> None:
    """
    Full pipeline: injection guard -> stage1 -> stage2 -> stage3 -> cost report.
    """
    print(f"\n{'='*60}")
    print(f"Processing: {document_name}")
    print("=" * 60)

    # Injection guard
    if check_injection(document_text):
        print("⚠️  BLOCKED: Prompt injection detected in document.")
        return

    costs = []

    # Stage 1
    print("Stage 1: Extracting entities...")
    result1, cost1 = stage1_extract_entities(document_text)
    if cost1:
        costs.append(cost1)
    if result1:
        print(f"  Found: {len(result1.people)} people, {len(result1.organizations)} orgs, {len(result1.monetary_amounts)} amounts")

    # Stage 2
    print("Stage 2: Classifying document...")
    result2, cost2 = stage2_classify_document(document_text, result1)
    if cost2:
        costs.append(cost2)
    if result2:
        print(f"  Type: {result2.document_type} (confidence: {result2.confidence:.0%})")

    # Stage 3
    print("Stage 3: Generating executive summary...")
    doc_type = result2.document_type if result2 else "document"
    result3, cost3 = stage3_generate_summary(document_text, doc_type, result1)
    if cost3:
        costs.append(cost3)
    if result3:
        print(f"\n  TITLE: {result3.title}")
        print("  KEY POINTS:")
        for point in result3.key_points[:3]:
            print(f"    • {point}")
        if result3.risk_flags:
            print(f"  ⚠️  RISKS: {', '.join(result3.risk_flags)}")
        print(f"  ACTION: {result3.action_required}")

    # Cost report
    total_cost = sum(c.cost_usd for c in costs)
    total_tokens = sum(c.input_tokens + c.output_tokens for c in costs)
    print(f"\n  COST REPORT: {total_tokens} total tokens | ${total_cost:.6f} USD")


if __name__ == "__main__":
    print("Intelligent Document Processor - Capstone Project")
    print("Processing 3 document types...\n")

    for doc_name, doc_text in DOCUMENTS.items():
        process_document(doc_text, doc_name.upper())

    print("\n" + "=" * 60)
    print("All documents processed successfully!")
