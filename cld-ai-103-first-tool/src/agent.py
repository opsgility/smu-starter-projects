"""Exercise 2 — build the agent loop.

Fill in the TWO TODOs to complete a working tool-calling agent. The
tools + implementations are already in tools.py — you only need to write
the LOOP that (a) reads response.stop_reason, (b) dispatches tool_use
blocks, (c) builds tool_result messages, (d) loops until end_turn.

Run standalone: `python src/agent.py "some user prompt"`
"""

import json
import os
import sys

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, os.path.dirname(__file__))
from tools import TOOL_SCHEMAS, TOOL_IMPLS


SYSTEM_PROMPT = """You are a support-triage agent for Orion Analytics. When
a user asks about a specific customer, use the get_customer_status tool to
look up their current state BEFORE making any decision. Never guess a
customer's tier, incident count, or status — always use the tool.

After you have the data you need, produce a short final answer explaining
your recommended action and the reasoning based on the tool results."""


def run_agent(client: anthropic.Anthropic, model: str, user_prompt: str,
              max_iterations: int = 10, verbose: bool = True) -> str:
    """Run the agent loop until end_turn or max_iterations hit. Returns the final text."""
    messages: list[dict] = [{"role": "user", "content": user_prompt}]

    for iteration in range(1, max_iterations + 1):
        if verbose:
            print(f"\n--- iteration {iteration} ---")

        response = client.messages.create(
            model=model,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )

        # TODO 1: append Claude's reply to messages.
        # HINT: messages.append({"role": "assistant", "content": response.content})
        # This preserves the tool_use blocks in the conversation history so
        # Claude sees them alongside the tool_result blocks you'll append
        # in TODO 2.
        pass  # <-- replace with the append line

        if verbose:
            print(f"stop_reason={response.stop_reason}")

        # Exit condition: Claude produced a final text answer, no more tools.
        if response.stop_reason == "end_turn":
            final_text = next((b.text for b in response.content if b.type == "text"), "")
            if verbose:
                print(f"final_text: {final_text}")
            return final_text

        # TODO 2: handle stop_reason == "tool_use".
        # For each tool_use block in response.content:
        #   - Look up the tool implementation in TOOL_IMPLS[block.name]
        #   - Call it with block.input (unpack with **block.input)
        #   - Build a tool_result block: {"type": "tool_result",
        #                                 "tool_use_id": block.id,
        #                                 "content": <the tool's return value>}
        #   - Collect all tool_result blocks into a list
        # Then append them as a single user-role message:
        #   messages.append({"role": "user", "content": tool_results})
        #
        # HINT: skeleton
        #   if response.stop_reason == "tool_use":
        #       tool_results = []
        #       for block in response.content:
        #           if block.type != "tool_use":
        #               continue
        #           if verbose:
        #               print(f"tool call: {block.name}({block.input})")
        #           impl = TOOL_IMPLS.get(block.name)
        #           if impl is None:
        #               result = json.dumps({"error": f"unknown tool: {block.name}"})
        #           else:
        #               result = impl(**block.input)
        #           if verbose:
        #               print(f"tool result: {result}")
        #           tool_results.append({
        #               "type": "tool_result",
        #               "tool_use_id": block.id,
        #               "content": result,
        #           })
        #       messages.append({"role": "user", "content": tool_results})
        #       continue  # loop back
        pass  # <-- replace with the tool_use handler above

    raise RuntimeError(f"Agent exceeded max_iterations={max_iterations} without end_turn.")


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: agent.py \"<user prompt>\"", file=sys.stderr)
        return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    final = run_agent(client, model, sys.argv[1], verbose=True)
    print(f"\n=== FINAL ANSWER ===\n{final}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
