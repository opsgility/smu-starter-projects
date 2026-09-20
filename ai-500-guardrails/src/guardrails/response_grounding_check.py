"""L4 output-response guardrail: groundedness + regulatory-phrase blocklist on the model's response.

You wire this in exercise 5. It is a `ChatMiddleware` that runs AFTER the model call
and short-circuits if the drafted response is unfounded or trips the regulatory regex.

Two independent sub-detectors run in this order:
  (a) Deterministic regulatory blocklist — regex `(?i)(guaranteed return|risk-free|
      insider information|guaranteed to grow)` on the response text. Any hit BLOCKs.
  (b) Groundedness detection — Azure AI Content Safety's `text:detectGroundedness`
      endpoint scores the response against the tool results the model consumed this
      turn. `ungroundedDetected == True and ungroundedPercentage > 0.05` BLOCKs.

The deterministic regex runs first because it is cheap and catches the highest-cost
failure modes (regulatory speech Ridge will personally sign a memo about).
"""
from __future__ import annotations
import os
import re

import httpx
from agent_framework import ChatContext, ChatMiddleware  # type: ignore
from azure.identity.aio import DefaultAzureCredential

REGULATORY_BLOCKLIST = re.compile(
    r"(?i)(guaranteed return|risk[- ]free|insider information|guaranteed to (grow|outperform|beat))"
)


class GuardrailBlocked(Exception):
    """Raised by any guardrail to short-circuit the flow with a user-visible reason."""


class ResponseGroundingCheck(ChatMiddleware):
    """Regulatory-phrase blocklist + Groundedness detection on the model's response."""

    UNGROUNDED_TOLERANCE = 0.05

    def __init__(self) -> None:
        self._endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"].rstrip("/")
        self._credential = DefaultAzureCredential()

    async def _bearer(self) -> str:
        token = await self._credential.get_token("https://cognitiveservices.azure.com/.default")
        return token.token

    async def process(self, context: ChatContext, call_next):  # noqa: D401
        await call_next()

        # TODO exercise 5 step 3: extract the model's drafted response text from context.
        # In agent-framework, the assistant reply lives at context.result.text (see the
        # RidgevaultOutputGuardrail example in the L9 teaching lab).
        response_text = ""  # <-- your code

        # (a) regulatory blocklist — cheap, run first
        # TODO exercise 5 step 4: if REGULATORY_BLOCKLIST.search(response_text) is not None,
        # raise GuardrailBlocked(f"Regulatory phrase detected: {match.group(0)!r}").

        # (b) groundedness detection
        tool_results = [m.text for m in context.messages if getattr(m, "role", "") == "tool"]
        if not tool_results:
            # Nothing to ground against — skip Groundedness detection but allow the response.
            return

        bearer = await self._bearer()
        payload = {
            "domain": "Generic",
            "task": "QnA",
            "text": response_text,
            "groundingSources": tool_results,
            "reasoning": False,
        }
        url = f"{self._endpoint}/contentsafety/text:detectGroundedness?api-version=2024-09-15-preview"
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.post(
                url,
                headers={"Authorization": f"Bearer {bearer}"},
                json=payload,
            )
            r.raise_for_status()
            result = r.json()

        # TODO exercise 5 step 5: if result["ungroundedDetected"] is True AND
        # result["ungroundedPercentage"] > self.UNGROUNDED_TOLERANCE, raise
        # GuardrailBlocked(f"Grounding failed: {result['ungroundedPercentage']:.0%} unfounded").
