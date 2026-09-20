"""Prompt-injection defense middleware — Exercise 6 Task 2 fills this in.

Contract: `guard(user_input: str) -> str` is called BEFORE the user text is
concatenated into the model call. Return either the sanitized text (safe to
forward), or raise ValueError with a short reason to short-circuit the call
and let the flow return a canned refusal.

Baseline behavior (before student edits): identity function — no defense.
"""
from __future__ import annotations

import re


# TODO(Exercise 6 Task 2): Replace this stub with real defense.
# Suggested checks — implement AT LEAST two:
#   1. Detect and strip "ignore previous instructions" / "system prompt" phrases.
#   2. Refuse if the input contains role-injection markers ("### system", "<|im_start|>system").
#   3. Truncate to a sane length (e.g. 4000 chars).
#   4. Block if the input tries to override the assistant role
#      (e.g. "you are now DAN", "act as a different assistant").
_INJECTION_PATTERNS: list[re.Pattern[str]] = [
    # e.g. re.compile(r"ignore (previous|prior|the above) (instructions|prompt)", re.I),
]


def guard(user_input: str) -> str:
    text = user_input or ""
    # for pat in _INJECTION_PATTERNS:
    #     if pat.search(text):
    #         raise ValueError(f"blocked by pattern: {pat.pattern}")
    return text
