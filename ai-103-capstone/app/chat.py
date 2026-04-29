"""/chat — stateless Summitline product/policy chat (Exercise 1)."""

from __future__ import annotations

import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from opentelemetry import trace

ENDPOINT = os.environ.get("AZURE_AI_PROJECT_ENDPOINT", "")
DEPLOYMENT = os.environ.get("MODEL_DEPLOYMENT", "gpt-4.1")

SYSTEM = (
    "You are the Summitline Outfitters concierge. Recommend gear, answer "
    "product questions, and stay on-brand: friendly, outdoorsy, concise. "
    "If a question needs order data or the knowledge base, say so plainly."
)

tracer = trace.get_tracer("summitline-capstone")


def reply(message: str) -> str:
    """Answer a single chat message using the Responses API.

    Uses :class:`AIProjectClient.get_openai_client` so the OpenAI SDK is
    pre-wired with ``DefaultAzureCredential`` against the Foundry project.

    Parameters
    ----------
    message : str
        The customer's question.

    Returns
    -------
    str
        The assistant text (``response.output_text``).
    """
    with tracer.start_as_current_span("summitline.chat.reply") as span:
        span.set_attribute("message.chars", len(message))

        # Exercise 1 - Step 7 Start
        raise NotImplementedError("Complete Exercise 1 Step 7")
        # Exercise 1 - Step 7 End
