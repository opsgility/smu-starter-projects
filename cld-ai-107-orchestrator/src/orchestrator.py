"""Orchestrator-worker pattern.

Orchestrator: decomposes a user question into 3 sub-questions using tool_use schema.
Workers: each answers one sub-question in parallel.
Synthesizer: aggregates 3 worker answers into a final synthesis.
"""

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
import anthropic


DECOMPOSE_SCHEMA = {
    "name": "submit_subquestions",
    "description": "Submit exactly 3 focused sub-questions that together answer the user's request.",
    "input_schema": {
        "type": "object",
        "properties": {
            "subquestions": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 3,
                "maxItems": 3,
            }
        },
        "required": ["subquestions"],
    }
}


def orchestrator_decompose(client, model: str, user_question: str) -> list[str]:
    """Ask Claude to break the question into 3 sub-questions."""
    prompt = (f"Break the following research question into EXACTLY 3 focused, non-overlapping "
              f"sub-questions that together answer it:\n\n{user_question}\n\nUse submit_subquestions.")
    resp = client.messages.create(
        model=model, max_tokens=512,
        tools=[DECOMPOSE_SCHEMA],
        tool_choice={"type": "tool", "name": "submit_subquestions"},
        messages=[{"role": "user", "content": prompt}],
    )
    block = next(b for b in resp.content if b.type == "tool_use")
    return list(block.input["subquestions"])


def worker_answer(client, model: str, sub_q: str) -> str:
    """One worker answers one sub-question."""
    # TODO: send sub_q as a user prompt with system prompt "You are a research assistant.
    # Answer the question in 2-3 concise sentences." Return the text.
    # HINT:
    #   resp = client.messages.create(model=model, max_tokens=300,
    #       system="You are a research assistant. Answer in 2-3 concise sentences.",
    #       messages=[{"role":"user","content": sub_q}])
    #   return next((b.text for b in resp.content if b.type == "text"), "")
    raise NotImplementedError("TODO: implement worker_answer")


def synthesizer(client, model: str, user_question: str, sub_qas: list[tuple[str, str]]) -> str:
    """Aggregate worker answers into a final synthesis."""
    formatted = "\n\n".join(f"Sub-question {i+1}: {q}\nAnswer: {a}" for i, (q, a) in enumerate(sub_qas))
    prompt = (f"Original question: {user_question}\n\n{formatted}\n\n"
              f"Synthesize a clear 4-sentence final answer that draws on all 3 sub-answers.")
    resp = client.messages.create(model=model, max_tokens=500,
                                  messages=[{"role":"user","content":prompt}])
    return next((b.text for b in resp.content if b.type == "text"), "")


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")

    q = "What are the main considerations when scaling a Claude-powered support bot from 100 to 100,000 tickets per day?"

    print(f"USER QUESTION: {q}\n")
    print("Orchestrator decomposing...")
    subqs = orchestrator_decompose(client, model, q)
    for i, s in enumerate(subqs, 1):
        print(f"  {i}. {s}")

    print("\nWorkers answering in parallel...")
    try:
        with ThreadPoolExecutor(max_workers=3) as pool:
            answers = list(pool.map(lambda sq: worker_answer(client, model, sq), subqs))
    except NotImplementedError as e:
        print(f"TODO not filled: {e}"); return 1

    print("\nWORKER ANSWERS:")
    for i, (sq, a) in enumerate(zip(subqs, answers), 1):
        print(f"\n[{i}] Q: {sq}\n    A: {a[:200]}...")

    print("\n\nSynthesizing final answer...")
    final = synthesizer(client, model, q, list(zip(subqs, answers)))
    print(f"\n=== FINAL ===\n{final}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
