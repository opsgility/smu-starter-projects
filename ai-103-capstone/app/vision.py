"""/vision-ask — multimodal Responses via AIProjectClient (Exercise 2)."""

from __future__ import annotations

import base64
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from opentelemetry import trace

ENDPOINT = os.environ.get("AZURE_AI_PROJECT_ENDPOINT", "")
DEPLOYMENT = os.environ.get("MODEL_DEPLOYMENT", "gpt-4.1")

tracer = trace.get_tracer("summitline-capstone")


def _data_url(image_bytes: bytes, mime: str = "image/jpeg") -> str:
    """Base64-encode ``image_bytes`` as a ``data:`` URL for Responses ``input_image``.

    Helper provided by the starter — do NOT rewrite.
    """
    b64 = base64.b64encode(image_bytes).decode("ascii")
    return f"data:{mime};base64,{b64}"


def ask(image_bytes: bytes, question: str) -> str:
    """Ask a multimodal question about an uploaded image.

    Uses the Responses API ``input_image`` content type so ``gpt-4.1`` can
    attend to the bytes directly.
    """
    with tracer.start_as_current_span("summitline.vision.ask") as span:
        span.set_attribute("image.bytes", len(image_bytes))
        span.set_attribute("question.chars", len(question))

        # TODO (Exercise 2 Step 3): open AIProjectClient(endpoint=ENDPOINT, credential=DefaultAzureCredential())
        # then the OpenAI client via project.get_openai_client().

        # TODO (Exercise 2 Step 3): call client.responses.create(model=DEPLOYMENT, input=[...])
        # where the single user message has a content array with two items:
        #   {"type": "input_text",  "text": question}
        #   {"type": "input_image", "image_url": _data_url(image_bytes)}
        # Return response.output_text.
        raise NotImplementedError(
            "Complete TODOs in app/vision.py (Exercise 2 Step 3)."
        )
