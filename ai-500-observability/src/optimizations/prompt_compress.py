"""Cheap deterministic prompt-compression pass for the risk_assessor system prompt.

The risk_assessor's system prompt in production carried a lot of legacy
verbiage: multiple restatements of the same rule, filler "please ensure that
you always" language, and long boilerplate signoffs. This module trims that
without changing semantics.

The compression is intentionally simple + deterministic so the lab can measure
its token impact reproducibly. A production system would use an LLM-based
compressor (or LLMLingua) — the shape is the same: input string in, shorter
string out, and the cost report shows the saving.
"""
from __future__ import annotations
import re
from dataclasses import dataclass

_FILLER_PATTERNS: list[tuple[str, str]] = [
    (r"(?i)\bplease ensure that you (always|never|do not|must)\b", r"\1"),
    (r"(?i)\bit is important to (note|understand|remember) that\b", ""),
    (r"(?i)\bas (an|a) (ai|assistant|analyst),?\s*", ""),
    (r"(?i)\bin order to\b", "to"),
    (r"(?i)\bat this (point in time|juncture)\b", "now"),
    (r"(?i)\bkindly\b", ""),
    (r"(?i)\bat your earliest convenience\b", "soon"),
    (r"\s{2,}", " "),
    (r"\n{3,}", "\n\n"),
]


@dataclass
class CompressionResult:
    original: str
    compressed: str
    original_chars: int
    compressed_chars: int

    @property
    def saved_chars(self) -> int:
        return self.original_chars - self.compressed_chars

    @property
    def saved_pct(self) -> float:
        if self.original_chars == 0:
            return 0.0
        return round(100.0 * self.saved_chars / self.original_chars, 2)


def compress_prompt(text: str) -> CompressionResult:
    """Return a shorter but semantically-equivalent version of `text`."""
    original = text
    out = text
    for pattern, replacement in _FILLER_PATTERNS:
        out = re.sub(pattern, replacement, out)
    out = out.strip()
    return CompressionResult(
        original=original,
        compressed=out,
        original_chars=len(original),
        compressed_chars=len(out),
    )
