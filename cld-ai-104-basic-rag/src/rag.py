"""Exercise 2 — implement the RAG generate step.

Fill in the TODO to compose a Claude prompt from the retrieved chunks
and produce a citation-shaped answer.

Run standalone: `python src/rag.py "What is the Sev-1 SLA?"`
"""

import json
import os
import re
import sys

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, os.path.dirname(__file__))
from retriever import retrieve


def _parse_answer_and_citations(text: str) -> dict:
    """Extract <answer>...</answer> and <citations><cite id=""/></citations> from text."""
    answer_match = re.search(r"<answer>(.*?)</answer>", text, re.DOTALL)
    cite_matches = re.findall(r'<cite\s+id="([^"]+)"\s*/?>', text)
    return {
        "answer": (answer_match.group(1).strip() if answer_match else ""),
        "citations": cite_matches,
        "raw": text,
    }


def rag_answer(client: anthropic.Anthropic, model: str, question: str, k: int = 5) -> dict:
    retrieved = retrieve(question, k=k)

    # TODO: build the prompt and call Claude. Requirements:
    #   - Wrap each retrieved chunk in <document id="{chunk['id']}">{chunk['text']}</document>
    #     tags, joined with newlines.
    #   - Compose a prompt that:
    #     - Instructs Claude to answer ONLY from provided documents
    #     - Instructs Claude to say "I don't know based on the provided sources" if the answer
    #       is not in the retrieved chunks
    #     - Requires <answer>...</answer> and <citations><cite id="..."/>...</citations> shape
    #   - Call client.messages.create() with the prompt
    #   - Extract text with the safe pattern from L1
    #   - Return {'answer': str, 'citations': list[str], 'retrieved_ids': list[str], 'raw': str}
    #
    # HINT skeleton:
    #   context = "\n\n".join(f'<document id="{c["id"]}">{c["text"]}</document>' for c in retrieved)
    #   prompt = f"""Answer using ONLY the documents below. If the answer is not in the documents,
    #   say "I don't know based on the provided sources."
    #
    #   {context}
    #
    #   Question: {question}
    #
    #   Reply inside these tags:
    #   <answer>your answer citing sources inline like [doc-id]</answer>
    #   <citations>
    #     <cite id="doc-id-1"/>
    #     <cite id="doc-id-2"/>
    #   </citations>"""
    #   response = client.messages.create(model=model, max_tokens=1024,
    #                                     messages=[{"role":"user","content":prompt}])
    #   text = next((b.text for b in response.content if b.type == "text"), "")
    #   parsed = _parse_answer_and_citations(text)
    #   return {**parsed, "retrieved_ids": [c["id"] for c in retrieved]}
    raise NotImplementedError("TODO: implement rag_answer")


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: rag.py \"<question>\""); return 2
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    r = rag_answer(client, model, sys.argv[1])
    print(json.dumps({"answer": r["answer"], "citations": r["citations"],
                     "retrieved_ids": r["retrieved_ids"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
