"""investment_researcher agent — Ridgevault Financial.

Owns open-ended research questions: sector outlooks, macro backdrop, the "why"
behind a portfolio recommendation. Answers MUST reflect Ridgevault's House View
voice and MUST cite Ridgevault research documents (never generic industry sources).

Exercise 2 — fill in SYSTEM_PROMPT with an advanced persona + few-shot block.
Exercise 5 — fill in the RAG grounding hook in `answer_with_grounding()`.
Exercise 6 — run `python -m src.agents.investment_researcher` and ask a portfolio
             question that requires document grounding.
"""
from __future__ import annotations
import os
import sys
from typing import List, Optional

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import OpenAI

# Sibling modules the exercises wire up.
try:
    from ..context_builder import trim_to_budget  # type: ignore
    from ..rag.foundry_iq_query import query_index  # type: ignore
except ImportError:
    # Allow running as a plain script (`python src/agents/investment_researcher.py`)
    # for smoke testing before the package layout is fully wired.
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from context_builder import trim_to_budget  # type: ignore
    from rag.foundry_iq_query import query_index  # type: ignore


# ---------------------------------------------------------------------------
# Exercise 2 — SYSTEM PROMPT
# ---------------------------------------------------------------------------
# TODO (Exercise 2): Rewrite SYSTEM_PROMPT with:
#   1. A persona block naming Ridgevault Financial, the House View voice, and the
#      audience (Ridgevault advisors reading in the CRM sidebar during client calls).
#   2. Explicit output contract: 3-5 sentence answers, House View verdict first,
#      supporting rationale second, one caveat third, citations last.
#   3. A refusal clause for questions outside Ridgevault's coverage universe
#      (crypto derivatives, individual stock timing, personal tax advice).
#   4. TWO few-shot exemplars — one sector question, one macro question — showing
#      the exact answer shape you want the model to imitate.
# The bare placeholder below produces the generic tropes the lesson is fixing.
SYSTEM_PROMPT = """You are a helpful investment research assistant. Answer the user's question."""


# ---------------------------------------------------------------------------
# Exercise 5 — RAG grounding
# ---------------------------------------------------------------------------
def build_messages(
    question: str,
    thread_history: List[dict],
    token_budget: int = 4000,
) -> List[dict]:
    """Assemble the messages array for one turn.

    Uses `trim_to_budget()` from context_builder (Exercise 3) to keep the running
    thread inside a token budget, and (Exercise 5) prepends grounded snippets
    from the Ridgevault research index so citations are enforceable.
    """
    trimmed_history = trim_to_budget(thread_history, token_budget)

    # TODO (Exercise 5): Retrieve grounded snippets for `question` via
    # `query_index(question, top_k=3)` and prepend them as a system message
    # framed as "Ridgevault research context. Cite these documents by title.".
    # For now, the agent runs with no grounding — Exercise 6 will show why that
    # matters when Compliance asks where a claim came from.
    grounded_context: Optional[str] = None

    messages: List[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
    if grounded_context:
        messages.append({"role": "system", "content": grounded_context})
    messages.extend(trimmed_history)
    messages.append({"role": "user", "content": question})
    return messages


def answer(question: str, thread_history: Optional[List[dict]] = None) -> str:
    """Ask investment_researcher one question and return its reply."""
    load_dotenv()
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    deployment = os.environ["FOUNDRY_MODEL"]

    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = OpenAI(
        base_url=f"{endpoint}/openai/v1",
        default_headers={"Authorization": f"Bearer {token_provider()}"},
        api_key="unused",
    )
    messages = build_messages(question, thread_history or [])
    resp = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_completion_tokens=600,
    )
    return (resp.choices[0].message.content or "").strip()


if __name__ == "__main__":
    q = " ".join(sys.argv[1:]) or (
        "A Ridgevault client with a 60/40 allocation asks whether to overweight "
        "energy for Q4 based on our current House View. What do you tell them?"
    )
    print(answer(q))
