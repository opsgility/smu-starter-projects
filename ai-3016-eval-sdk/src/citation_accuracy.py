"""AI-3016 Lesson 16 — custom citation-accuracy evaluator.

Built-in Groundedness answers "is the answer grounded in the retrieved
context somewhere?" It does NOT answer "does each [1] [2] citation MARKER
point at the chunk that supports THAT specific claim?"

This evaluator checks the citation markers themselves. For each numbered
citation in the answer, we verify that the cited chunk contains textual
overlap with the surrounding claim.
"""

from __future__ import annotations

import re
from typing import Iterable


def _extract_citations(answer: str) -> list[int]:
    """Return the list of citation indexes referenced in the answer (e.g., [1] [3])."""
    return [int(n) for n in re.findall(r"\[(\d+)\]", answer)]


def _overlap_score(claim: str, chunk_content: str) -> float:
    """Compute lightweight token overlap 0-1 between claim + chunk.

    A real implementation might embed both and use cosine similarity, or
    call a small LLM to grade. For a cheap deterministic starter, we use
    Jaccard on lowercased tokens ignoring short/stopwords.
    """
    stop = {"a", "an", "the", "of", "in", "on", "and", "or", "to", "is", "for", "with", "by", "as"}
    tok_claim = {w for w in re.findall(r"[a-z]{3,}", claim.lower()) if w not in stop}
    tok_chunk = {w for w in re.findall(r"[a-z]{3,}", chunk_content.lower()) if w not in stop}
    if not tok_claim or not tok_chunk:
        return 0.0
    return len(tok_claim & tok_chunk) / max(len(tok_claim), 1)


def citation_accuracy(*, response: str, context: Iterable[dict]) -> dict:
    """Score citation accuracy for one flow output.

    Args:
        response: the model's answer text (may contain [1], [2] markers).
        context: iterable of retrieved chunks; each dict has at least "content".

    Returns:
        {"citation_accuracy": float in [0, 1], "citations_checked": int}
        Score is 1.0 when every citation's target chunk has strong overlap
        with the surrounding claim, 0.0 when none do.
    """
    context_list = list(context)
    citations = _extract_citations(response)
    if not citations:
        # No citations to check -- neutral 1.0 (nothing wrong per se).
        return {"citation_accuracy": 1.0, "citations_checked": 0}

    total_score = 0.0
    checked = 0
    for cite in citations:
        idx = cite - 1  # citations are 1-indexed in the prompt
        if 0 <= idx < len(context_list):
            chunk_text = context_list[idx].get("content", "")
            # Grab the sentence containing this citation as the "claim."
            claim_match = re.search(
                rf"([^.!?]*\[{cite}\][^.!?]*[.!?])",
                response,
                re.DOTALL,
            )
            claim = claim_match.group(1) if claim_match else response
            total_score += _overlap_score(claim, chunk_text)
            checked += 1

    accuracy = total_score / max(checked, 1)
    return {"citation_accuracy": round(accuracy, 3), "citations_checked": checked}


if __name__ == "__main__":
    # Quick local test.
    example_context = [
        {"content": "Aurora's kickoff phase runs two to three weeks including stakeholder mapping."},
        {"content": "The escalation path for complaints starts with the engagement manager."},
    ]
    example_answer = "Aurora's kickoff runs 2-3 weeks including stakeholder mapping [1]. For complaints, contact the engagement manager first [2]."
    print(citation_accuracy(response=example_answer, context=example_context))
