"""L3 tool-result guardrail: redacts PII from `client_record` / `portfolio_lookup` returns.

You wire this in exercise 4. It is a `FunctionMiddleware` that runs AFTER the tool
executes and BEFORE the model sees the result. Uses Azure AI Language's PII entity
recognition to detect and redact SSN, DOB, phone, address, and person names in-place.

Auth: DefaultAzureCredential + Cognitive Services User on the Language account.
Fail policy: FAIL_CLOSED — if Language returns an error, propagate and let the
runtime deny the response rather than let the raw tool result reach the model.
"""
from __future__ import annotations
import json
import os

from agent_framework import FunctionInvocationContext, FunctionMiddleware  # type: ignore
from azure.ai.textanalytics.aio import TextAnalyticsClient  # type: ignore
from azure.identity.aio import DefaultAzureCredential

REDACTED_TOOLS = {"client_record", "portfolio_lookup"}

# Ridgevault PII categories — trimmed to what actually appears in the tool payloads.
PII_CATEGORIES = ["USSocialSecurityNumber", "DateTime", "PhoneNumber", "Address", "Person"]


class ToolResultPiiRedact(FunctionMiddleware):
    """Runs Azure AI Language PII recognition on the tool return; replaces detected spans with tags."""

    def __init__(self) -> None:
        endpoint = os.environ["LANGUAGE_ENDPOINT"]
        self._client = TextAnalyticsClient(endpoint=endpoint, credential=DefaultAzureCredential())

    async def process(self, context: FunctionInvocationContext, call_next):  # noqa: D401
        await call_next()  # let the tool run first

        if context.function.name not in REDACTED_TOOLS:
            return

        raw = context.result
        # TODO exercise 4 step 2: coerce raw to a JSON string via json.dumps if it is not already a string.
        text = raw if isinstance(raw, str) else json.dumps(raw)

        # TODO exercise 4 step 3: call self._client.recognize_pii_entities([text],
        # categories_filter=PII_CATEGORIES). Iterate result[0].entities; use `redacted_text`
        # from the SDK response for the transformed output.
        # Example of expected shape when SSN + Person are found:
        #   { "name": "***", "ssn": "***-**-****", "balance": 1240382 }

        # After redaction, if the original raw was a dict, parse the redacted JSON string
        # back into a dict so downstream tool_result shape matches. Otherwise assign the string.
        # context.result = <redacted-shape>
