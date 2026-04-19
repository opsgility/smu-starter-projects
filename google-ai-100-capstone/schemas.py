"""Pydantic schemas for capstone structured output."""
from typing import List
from pydantic import BaseModel, Field


class CatalogEntry(BaseModel):
    headline: str
    description: str = Field(description="2-4 sentences, tone-compliant")
    feature_bullets: List[str] = Field(description="3-5 short bullets")
    target_customer: str = Field(description="One sentence")


class FAQItem(BaseModel):
    question: str
    answer: str


class AssistBundle(BaseModel):
    sku: str
    summary: str = Field(description="One customer-friendly sentence")
    catalog: CatalogEntry
    faq: List[FAQItem] = Field(description="Exactly 3 items")
