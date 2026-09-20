"""Dynamic-context builder for Ridgevault multi-agent threads.

A long-running Ridgevault advisory thread accumulates dozens of turns per client.
Sending the whole history on every call blows the model's context window and
inflates cost. `trim_to_budget()` keeps the thread inside a token budget while
preserving the messages that matter for continuity.

Exercise 3 — implement `trim_to_budget()` per the docstring contract.
"""
from __future__ import annotations
from typing import List

import tiktoken


def _count_tokens(text: str, model_hint: str = "gpt-4o") -> int:
    """Approximate token count using tiktoken.

    `gpt-4o`'s encoding is a reasonable stand-in for gpt-5 family models —
    tiktoken doesn't ship a gpt-5-specific encoder yet, and the count is used
    only for budgeting (a ~5% drift is well inside the safety margin).
    """
    try:
        enc = tiktoken.encoding_for_model(model_hint)
    except KeyError:
        enc = tiktoken.get_encoding("o200k_base")
    return len(enc.encode(text))


def message_tokens(message: dict) -> int:
    """Rough token cost of one chat message (content + ~4 for role/formatting)."""
    return _count_tokens(str(message.get("content", ""))) + 4


def trim_to_budget(
    thread_history: List[dict],
    token_budget: int,
) -> List[dict]:
    """Return a trimmed copy of thread_history that fits inside token_budget.

    Contract (Exercise 3 TODO):
      1. Preserve every message with role == "system" — they carry Ridgevault's
         persona + grounding and must never be dropped.
      2. Preserve the FIRST user message in the thread — it's the client's
         original brief; agents lose the plot without it.
      3. Preserve the LAST user + LAST assistant message — the immediate turn
         context.
      4. Fill the remaining budget with the MOST RECENT messages between the
         preserved first-user and last-user, dropping oldest first.
      5. Return messages in their original order.
      6. If token_budget is impossibly small (< sum of the required preserves),
         still return the required preserves — never drop rules 1-3.

    The starter body below is a naive placeholder that returns the whole
    thread unchanged. Replace it.
    """
    # TODO (Exercise 3): Replace this placeholder with the contract above.
    return list(thread_history)
