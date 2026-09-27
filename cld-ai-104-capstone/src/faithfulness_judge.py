"""Exercise 2 — LLM-judge for RAG faithfulness (L9 pattern)."""

import anthropic


JUDGE_SCHEMA = {
    "name": "submit_faithfulness_verdict",
    "description": "Judge whether the answer's claims are supported by the retrieved chunks.",
    "input_schema": {
        "type": "object",
        "properties": {
            "overall_faithfulness_score": {"type": "number", "minimum": 0, "maximum": 1,
                                           "description": "Fraction of claims grounded in the chunks."},
            "reasoning": {"type": "string"}
        },
        "required": ["overall_faithfulness_score", "reasoning"],
        "additionalProperties": False
    }
}


def judge_faithfulness(client: anthropic.Anthropic, model: str, question: str,
                       answer: str, retrieved_chunks: list[dict]) -> dict:
    """Return {'overall_faithfulness_score': float, 'reasoning': str}."""
    chunks_text = "\n\n".join(f'<chunk id="{c["id"]}">{c["text"]}</chunk>' for c in retrieved_chunks)

    # TODO: call client.messages.create with:
    #   tools=[JUDGE_SCHEMA]
    #   tool_choice={"type":"tool","name":"submit_faithfulness_verdict"}
    #   messages=[{"role":"user","content": prompt}]
    #   where prompt describes the task: given question, answer, and chunks,
    #   score the fraction of claims in the answer supported by the chunks (0.0-1.0).
    # Then find tool_use block and return dict(block.input).
    #
    # HINT:
    #   prompt = f"""Question: {question}
    #
    #   Retrieved chunks:
    #   {chunks_text}
    #
    #   Answer to evaluate:
    #   {answer}
    #
    #   Score the fraction of claims in the answer that are supported by
    #   the retrieved chunks. 1.0 = every claim grounded; 0.0 = no claims grounded.
    #   Use submit_faithfulness_verdict."""
    #   resp = client.messages.create(model=model, max_tokens=512,
    #       tools=[JUDGE_SCHEMA],
    #       tool_choice={"type":"tool","name":"submit_faithfulness_verdict"},
    #       messages=[{"role":"user","content":prompt}])
    #   block = next(b for b in resp.content if b.type == "tool_use")
    #   return dict(block.input)
    raise NotImplementedError("TODO: implement judge_faithfulness")
