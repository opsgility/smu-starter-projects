"""L1 input guardrail: Azure AI Content Safety (harm categories) + Prompt Shields (injection).

You wire this in exercise 2. It is a `ChatMiddleware` that runs BEFORE the model call
and short-circuits on any of:
  - Prompt Shields `userPromptAnalysis.attackDetected == true`
  - Content Safety severity >= 2 on Hate / SelfHarm / Sexual / Violence

Auth: DefaultAzureCredential + Cognitive Services User role on the Content Safety account.
Fail policy: FAIL_CLOSED (any exception propagates — the runtime denies).
"""
from __future__ import annotations
import os

from agent_framework import ChatContext, ChatMiddleware  # type: ignore
from azure.ai.contentsafety.aio import ContentSafetyClient  # type: ignore
from azure.ai.contentsafety.models import (  # type: ignore
    AnalyzeTextOptions,
    ShieldPromptOptions,
    TextCategory,
)
from azure.identity.aio import DefaultAzureCredential


class GuardrailBlocked(Exception):
    """Raised by any guardrail to short-circuit the flow with a user-visible reason."""


class InputContentSafetyGuardrail(ChatMiddleware):
    """Runs Prompt Shields + Content Safety on the last user message. BLOCKs on positive."""

    # Ridgevault threshold: block Low+ (severity >= 2). Adjust per category if needed.
    SEVERITY_THRESHOLD = 2

    def __init__(self) -> None:
        endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]
        self._client = ContentSafetyClient(endpoint=endpoint, credential=DefaultAzureCredential())

    async def process(self, context: ChatContext, call_next):  # noqa: D401
        # TODO exercise 2 step 3: extract the last user message text from context.messages
        user_text = ""  # <-- your code
        if not user_text:
            await call_next()
            return

        # TODO exercise 2 step 4: call Prompt Shields via self._client.shield_prompt(...)
        # Raise GuardrailBlocked("Prompt injection detected") if userPromptAnalysis.attackDetected is True.

        # TODO exercise 2 step 5: call Content Safety text analyze via self._client.analyze_text(...)
        # Iterate categoriesAnalysis; if any severity >= SEVERITY_THRESHOLD, raise
        # GuardrailBlocked(f"Harmful content: {category} severity {sev}").

        await call_next()  # only reached on ALLOW
