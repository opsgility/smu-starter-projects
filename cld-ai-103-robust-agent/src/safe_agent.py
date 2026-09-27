"""Exercise 2 — robust agent with safe_execute + retry + circuit breakers.

Fill in the THREE TODOs to layer three defenses on top of the L4 agent shape:
  1. execute_with_retry — retries only transient errors with exponential backoff.
  2. safe_execute — wraps tool calls, catches all exceptions, returns error tool_result.
  3. run_agent — enforces max_iterations + max_tool_calls circuit breakers.

Run standalone: `python src/safe_agent.py "some user prompt"`
"""

import json
import os
import sys
import time
import logging

from dotenv import load_dotenv
import anthropic

sys.path.insert(0, os.path.dirname(__file__))
from flaky_tools import TOOL_SCHEMAS, TOOL_IMPLS, TransientToolError, PermanentToolError


logger = logging.getLogger("safe_agent")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


SYSTEM_PROMPT = """You are a support-triage agent for Orion Analytics. Use the
4 tools available. Chain tools as needed; when a tool returns an error, read
it and decide whether to retry with different input, try a different tool,
or escalate. End with a short summary."""


TRANSIENT_STATUS = {429, 500, 502, 503, 504}


def _is_transient(e: Exception) -> bool:
    if isinstance(e, TransientToolError):
        return True
    return getattr(e, "status_code", None) in TRANSIENT_STATUS


def execute_with_retry(impl, kwargs, max_attempts: int = 4) -> str:
    # TODO 1: implement exponential-backoff retry.
    # Requirements:
    #   - Loop up to max_attempts times.
    #   - Call impl(**kwargs) inside a try/except.
    #   - On TransientToolError (or _is_transient returning True), sleep 2**(attempt-1) seconds and retry.
    #   - On any other exception OR on final attempt, re-raise (safe_execute will catch it).
    #   - Return the impl's result on success.
    #
    # HINT: skeleton
    #   for attempt in range(1, max_attempts + 1):
    #       try:
    #           return impl(**kwargs)
    #       except Exception as e:
    #           if not _is_transient(e) or attempt == max_attempts:
    #               raise
    #           sleep_s = 2 ** (attempt - 1)
    #           logger.info(f"retry {attempt}/{max_attempts} after {sleep_s}s for {impl.__name__}: {e}")
    #           time.sleep(sleep_s)
    raise NotImplementedError("TODO 1: implement execute_with_retry")


def safe_execute(block) -> dict:
    # TODO 2: build a tool_result block for one tool_use, catching ANY exception.
    # Requirements:
    #   - Look up impl in TOOL_IMPLS[block.name]; if missing, error tool_result.
    #   - Call execute_with_retry(impl, block.input, max_attempts=4).
    #   - Wrap in try/except; on exception, log with logger.exception(...) THEN
    #     return a tool_result with content=JSON error dict.
    #   - On success, return tool_result with content=result string.
    #
    # HINT: skeleton
    #   impl = TOOL_IMPLS.get(block.name)
    #   if impl is None:
    #       return {"type": "tool_result", "tool_use_id": block.id,
    #               "content": json.dumps({"error": f"unknown tool: {block.name}"})}
    #   try:
    #       result = execute_with_retry(impl, dict(block.input))
    #   except Exception as e:
    #       logger.exception(f"tool {block.name} failed with input {block.input}")
    #       result = json.dumps({"error": str(e), "exception_type": type(e).__name__})
    #   return {"type": "tool_result", "tool_use_id": block.id, "content": result}
    raise NotImplementedError("TODO 2: implement safe_execute")


def run_agent(client: anthropic.Anthropic, model: str, user_prompt: str,
              max_iterations: int = 15, max_tool_calls: int = 50) -> dict:
    """Runs the agent with dual circuit breakers."""
    messages: list[dict] = [{"role": "user", "content": user_prompt}]
    tool_call_count = 0

    for iteration in range(1, max_iterations + 1):
        response = client.messages.create(
            model=model, max_tokens=1024,
            system=SYSTEM_PROMPT, tools=TOOL_SCHEMAS, messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            final_text = next((b.text for b in response.content if b.type == "text"), "")
            return {"final_text": final_text, "iterations": iteration,
                    "tool_call_count": tool_call_count, "circuit_tripped": None}

        tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
        tool_call_count += len(tool_use_blocks)

        # TODO 3: circuit breaker — if tool_call_count > max_tool_calls, inject a
        # synthetic tool_result telling Claude the budget is exhausted, then let the
        # loop iterate ONE more time so Claude produces a final answer.
        #
        # HINT:
        #   if tool_call_count > max_tool_calls:
        #       tool_results = [{"type": "tool_result",
        #                        "tool_use_id": tool_use_blocks[0].id,
        #                        "content": json.dumps({"error": "tool-call budget exhausted; produce a final answer now"}),
        #                        "is_error": True}]
        #       messages.append({"role": "user", "content": tool_results})
        #       # Force one more Claude call to produce end_turn
        #       response = client.messages.create(
        #           model=model, max_tokens=1024,
        #           system=SYSTEM_PROMPT, tools=TOOL_SCHEMAS, messages=messages,
        #       )
        #       messages.append({"role": "assistant", "content": response.content})
        #       final_text = next((b.text for b in response.content if b.type == "text"), "")
        #       return {"final_text": final_text, "iterations": iteration + 1,
        #               "tool_call_count": tool_call_count, "circuit_tripped": "max_tool_calls"}

        tool_results = [safe_execute(block) for block in tool_use_blocks]
        messages.append({"role": "user", "content": tool_results})

    # max_iterations exhausted without end_turn
    return {"final_text": "(agent hit max_iterations without producing a final answer)",
            "iterations": max_iterations, "tool_call_count": tool_call_count,
            "circuit_tripped": "max_iterations"}


def main() -> int:
    load_dotenv()
    if len(sys.argv) < 2:
        print("usage: safe_agent.py \"<prompt>\""); return 2
    client = anthropic.Anthropic()
    result = run_agent(client, os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5"), sys.argv[1])
    print(f"iterations={result['iterations']}  tool_calls={result['tool_call_count']}  circuit={result['circuit_tripped']}")
    print(f"\n=== FINAL ===\n{result['final_text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
