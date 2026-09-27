"""Exercise 2 — sequential 4-tool agent.

Fill in the ONE TODO: run the L2-shape agent loop with 4 tools instead
of 1. The mechanics are identical (append assistant reply, dispatch
tool_use blocks, append tool_results, loop until end_turn); the delta
is that Claude will chain 2-4 tool calls per scenario.

Run standalone: `python src/agent_sequential.py "some user prompt"`
"""

import json
import os
import sys

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, os.path.dirname(__file__))
from tools import TOOL_SCHEMAS, TOOL_IMPLS


SYSTEM_PROMPT = """You are a support-triage agent for Orion Analytics. You have
four tools: get_customer_status, search_recent_tickets, apply_refund,
escalate_to_human. Follow this general workflow:

1. For any customer-specific request, call get_customer_status FIRST.
2. For Pro or Enterprise customers, follow up with search_recent_tickets
   to understand the pattern.
3. Based on the customer state + ticket history, either apply_refund (if
   warranted AND account is active) OR escalate_to_human (if the
   situation requires human judgment).
4. End with a short summary of the actions you took."""


def run_agent(client: anthropic.Anthropic, model: str, user_prompt: str,
              max_iterations: int = 10) -> dict:
    """Return {'final_text': str, 'iterations': int, 'tool_calls': [(name, input)]}."""
    messages: list[dict] = [{"role": "user", "content": user_prompt}]
    tool_calls: list[tuple] = []

    for iteration in range(1, max_iterations + 1):
        response = client.messages.create(
            model=model, max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            final_text = next((b.text for b in response.content if b.type == "text"), "")
            return {"final_text": final_text, "iterations": iteration, "tool_calls": tool_calls}

        # TODO: handle stop_reason == "tool_use". For each tool_use block:
        #   - Track the call in tool_calls list (name + input)
        #   - Dispatch to TOOL_IMPLS[block.name](**block.input)
        #   - Build tool_result block referencing block.id
        # Then append all tool_result blocks as a single user-role message.
        #
        # HINT: skeleton
        #   tool_results = []
        #   for block in response.content:
        #       if block.type != "tool_use":
        #           continue
        #       tool_calls.append((block.name, dict(block.input)))
        #       impl = TOOL_IMPLS.get(block.name)
        #       if impl is None:
        #           result = json.dumps({"error": f"unknown tool: {block.name}"})
        #       else:
        #           result = impl(**block.input)
        #       tool_results.append({
        #           "type": "tool_result",
        #           "tool_use_id": block.id,
        #           "content": result,
        #       })
        #   messages.append({"role": "user", "content": tool_results})
        pass  # <-- replace

    raise RuntimeError(f"agent exceeded max_iterations={max_iterations}")


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: agent_sequential.py \"<user prompt>\""); return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    result = run_agent(client, model, sys.argv[1])
    print(f"iterations: {result['iterations']}")
    print(f"tool_calls: {result['tool_calls']}")
    print(f"\n=== FINAL ANSWER ===\n{result['final_text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
