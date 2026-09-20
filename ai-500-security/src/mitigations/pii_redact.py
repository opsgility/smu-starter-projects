"""PII redaction filter — Exercise 6 Task 3 fills this in.

Contract: `redact(model_output: str) -> str` is called AFTER the model reply
comes back but BEFORE it is returned to the caller. Replace anything that
looks like PII (SSNs, credit cards, emails, phone numbers) with a placeholder
so the response never leaks it downstream.

Baseline behavior (before student edits): identity function — no redaction.
"""
from __future__ import annotations

import re


# TODO(Exercise 6 Task 3): Replace this stub with real redaction.
# Redact AT LEAST these three patterns and add SSN/card as bonus:
#   - Email addresses          → <email>
#   - US phone numbers         → <phone>
#   - Credit card-ish digits   → <card>
#   - SSN                       → <ssn>
_REDACT_RULES: list[tuple[re.Pattern[str], str]] = [
    # (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "<ssn>"),
    # (re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I), "<email>"),
]


def redact(model_output: str) -> str:
    out = model_output or ""
    # for pat, placeholder in _REDACT_RULES:
    #     out = pat.sub(placeholder, out)
    return out
