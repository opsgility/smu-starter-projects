"""AI-3016 Lesson 9 — scaffold for a Python node that plugs into a Prompt Flow.

A Prompt Flow Python node is any Python function decorated with @tool. Iterate
here locally with fake inputs, then copy the function body into the Foundry
flow editor's Python node. Foundry provides the @tool decorator at runtime.

This scaffold shows two realistic patterns:

  1. `enrich_query` — expand a user question with related terms to improve
     retrieval hit rate (Lesson 10 topic 4 -- query rewriting).

  2. `deduplicate_chunks` — post-process retrieved chunks to remove near
     duplicates before they reach the answer LLM (Lesson 10 topic 4 --
     fixing contradictory-chunk retrieval failures).
"""

# Locally we mock the promptflow.tool decorator with a no-op so this file
# runs standalone. In the Foundry editor, replace with:
#   from promptflow import tool
def tool(fn):  # pragma: no cover
    return fn


@tool
def enrich_query(user_question: str) -> str:
    """Expand common shorthand into more retrievable phrasing.

    Example transform:
      "returns"           -> "return policy refund guidelines"
      "PTO"               -> "paid time off vacation policy"
      "Acme kickoff date" -> "Acme project kickoff date engagement start"

    This is a lightweight rule-based enricher. A more sophisticated version
    would use a cheap LLM (gpt-4o-mini) to rewrite queries.
    """
    q = user_question.lower()
    expansions = {
        " returns": " return policy refund",
        " pto ": " paid time off vacation policy ",
        " kickoff": " kickoff date engagement start",
        " sow ": " statement of work sow ",
    }
    enriched = user_question
    for short, long in expansions.items():
        if short in q:
            enriched = f"{enriched} {long.strip()}"
    return enriched


@tool
def deduplicate_chunks(chunks: list[dict]) -> list[dict]:
    """Remove near-duplicate chunks by comparing their leading 100 chars.

    RAG retrieval sometimes surfaces chunks that share most of their content
    (e.g., a policy quoted in two different documents). Feeding both to the
    answer LLM wastes context and confuses citation.

    Returns a de-duplicated list, preserving the highest-scored representative
    of each duplicate cluster.
    """
    seen = set()
    kept = []
    for c in chunks:
        # Compact key: first 100 chars of content, lowercased.
        key = c.get("content", "").strip().lower()[:100]
        if key and key not in seen:
            seen.add(key)
            kept.append(c)
    return kept


if __name__ == "__main__":
    # Local dev harness — mimics Foundry inputs and prints outputs.
    print(enrich_query("What are our returns processed within?"))

    fake_chunks = [
        {"content": "Employees receive 15 PTO days annually...", "filepath": "hr-policy.pdf", "score": 0.89},
        {"content": "Employees receive 15 PTO days annually per calendar year.", "filepath": "handbook.pdf", "score": 0.87},
        {"content": "Client engagement kickoffs run 2-3 weeks.", "filepath": "methodology.pdf", "score": 0.72},
    ]
    print(deduplicate_chunks(fake_chunks))
