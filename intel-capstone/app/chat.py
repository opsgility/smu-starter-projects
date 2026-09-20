"""/chat — stateless SIB OSINT Concierge analyst chat (Exercise 1)."""

from __future__ import annotations

import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from opentelemetry import trace

ENDPOINT = os.environ.get("AZURE_AI_PROJECT_ENDPOINT", "")
DEPLOYMENT = os.environ.get("MODEL_DEPLOYMENT", "gpt-5")

SYSTEM = (
    "You are the Sentinel Intelligence Bureau OSINT Concierge. Help analysts "
    "summarize unclassified open-source signals, answer handbook and policy "
    "questions, and stay on-brand: precise, sober, concise. If a question "
    "needs indicator data or the policy knowledge base, say so plainly."
)

tracer = trace.get_tracer("sib-osint-capstone")


def reply(message: str) -> str:
    """Answer a single chat message using the Responses API.

    Uses :class:`AIProjectClient.get_openai_client` so the OpenAI SDK is
    pre-wired with ``DefaultAzureCredential`` against the Foundry project.

    Parameters
    ----------
    message : str
        The analyst's question.

    Returns
    -------
    str
        The assistant text (``response.output_text``).
    """
    with tracer.start_as_current_span("sib.chat.reply") as span:
        span.set_attribute("message.chars", len(message))

        # Exercise 1 - Step 7 Start
        raise NotImplementedError("Complete Exercise 1 Step 7")
        # Exercise 1 - Step 7 End
