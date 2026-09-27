"""Exercise 3 — parallelize independent tool calls with ThreadPoolExecutor.

Fill in the TWO TODOs to (1) build a per-block execution function and
(2) execute all tool_use blocks in Claude's response concurrently.

The API-side change is the SAME as sequential — Claude may emit multiple
tool_use blocks in one response. What differs is your dispatch: instead
of `for block: result = impl(**block.input)` in sequence, you use
ThreadPoolExecutor.map to run them concurrently.

Latency win only shows when Claude actually emits 2+ tool_use blocks in
one response. Add a hint to the system prompt if Claude keeps splitting
one-at-a-time.

Run standalone: `python src/agent_parallel.py "some user prompt"`
"""

import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, os.path.dirname(__file__))
from tools import TOOL_SCHEMAS, TOOL_IMPLS


SYSTEM_PROMPT = """You are a support-triage agent for Orion Analytics. You have
four tools: get_customer_status, search_recent_tickets, apply_refund,
escalate_to_human.

CRITICAL: when you need multiple INDEPENDENT lookups (e.g., customer
status AND recent tickets for the same customer), request them ALL in
ONE response. This lets the client execute them in parallel and cuts
latency in half.

Only chain sequentially when the next tool's input DEPENDS on the
previous tool's output.

End with a short summary of the actions you took."""


def _execute_one(block, tool_calls_log: list) -> dict:
    """Execute one tool_use block and return its tool_result dict."""
    tool_calls_log.append((block.name, dict(block.input)))
    impl = TOOL_IMPLS.get(block.name)
    if impl is None:
        result = json.dumps({"error": f"unknown tool: {block.name}"})
    else:
        result = impl(**block.input)
    return {"type": "tool_result", "tool_use_id": block.id, "content": result}


def run_agent(client: anthropic.Anthropic, model: str, user_prompt: str,
              max_iterations: int = 10) -> dict:
    messages: list[dict] = [{"role": "user", "content": user_prompt}]
    tool_calls: list[tuple] = []
    tool_wall_time_ms = 0

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
            return {"final_text": final_text, "iterations": iteration,
                    "tool_calls": tool_calls, "tool_wall_time_ms": tool_wall_time_ms}

        # TODO 1: extract the list of tool_use blocks from response.content.
        # HINT: tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
        tool_use_blocks = []  # <-- replace

        # TODO 2: execute all tool_use_blocks in PARALLEL using
        # ThreadPoolExecutor.map. Time the parallel dispatch (t0 = time.perf_counter()
        # before, tool_wall_time_ms += int((time.perf_counter()-t0)*1000) after).
        #
        # HINT: skeleton
        #   t0 = time.perf_counter()
        #   with ThreadPoolExecutor(max_workers=8) as pool:
        #       tool_results = list(pool.map(lambda b: _execute_one(b, tool_calls), tool_use_blocks))
        #   tool_wall_time_ms += int((time.perf_counter() - t0) * 1000)
        #   messages.append({"role": "user", "content": tool_results})
        pass  # <-- replace

    raise RuntimeError(f"agent exceeded max_iterations={max_iterations}")


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: agent_parallel.py \"<user prompt>\""); return 2
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
    client = anthropic.Anthropic()
    t0 = time.perf_counter()
    result = run_agent(client, model, sys.argv[1])
    total_ms = int((time.perf_counter() - t0) * 1000)
    print(f"iterations: {result['iterations']}  tool_wall_time_ms: {result['tool_wall_time_ms']}  total_ms: {total_ms}")
    print(f"tool_calls: {result['tool_calls']}")
    print(f"\n=== FINAL ANSWER ===\n{result['final_text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
