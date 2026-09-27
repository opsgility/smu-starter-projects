"""LLM-judge on 3 criteria: relevance, tone, correctness."""

import os, sys
from dotenv import load_dotenv
import anthropic


SCHEMA = {"name":"submit_verdict",
  "input_schema":{"type":"object",
    "properties":{"passed":{"type":"boolean"},"reasoning":{"type":"string"}},
    "required":["passed","reasoning"], "additionalProperties":False}}


CRITERIA = [
    "The answer directly addresses the customer's question.",
    "The tone is professional and respectful even if the customer is frustrated.",
    "The answer avoids making up unsupported claims about policies or capabilities.",
]

ANSWER = ("I understand the frustration around the dashboard being down. Let me look into it "
          "right away — I'll check the ingest pipeline and status of the /v2/analytics endpoint "
          "and follow up within 30 minutes with next steps.")
QUESTION = "My dashboard has been down for 40 minutes. What can you do?"


def judge(client, model, answer: str, criterion: str) -> dict:
    prompt = f"Question: {QUESTION}\n\nAnswer:\n{answer}\n\nCriterion: {criterion}\n\nDoes the answer satisfy the criterion?"
    resp = client.messages.create(model=model, max_tokens=400,
        tools=[SCHEMA], tool_choice={"type":"tool","name":"submit_verdict"},
        messages=[{"role":"user","content": prompt}])
    return dict(next(b.input for b in resp.content if b.type == "tool_use"))


def main():
    load_dotenv()
    client = anthropic.Anthropic()
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    for c in CRITERIA:
        v = judge(client, model, ANSWER, c)
        print(f"\n{c}\n  {'✓' if v['passed'] else '✗'}  {v['reasoning'][:150]}")


if __name__ == "__main__":
    main()
