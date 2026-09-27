"""Exercise 3 — eval harness with deterministic + LLM-judge scoring."""

import json
import os
import sys

import anthropic


JUDGE_SCHEMA = {
    "name": "submit_verdict",
    "description": "Submit judgment for one semantic criterion.",
    "input_schema": {
        "type": "object",
        "properties": {
            "passed": {"type": "boolean"},
            "reasoning": {"type": "string"}
        },
        "required": ["passed", "reasoning"],
        "additionalProperties": False
    }
}


def score_deterministic(result: dict, expected: dict) -> dict:
    """Return {'checks': [...], 'passed': bool}."""
    checks = []
    action_record = result.get("action_record") or {}
    tools_used = result.get("tools_used") or []

    # Check 1: expected_action match (if specified)
    exp_action = expected.get("expected_action")
    if exp_action:
        got = action_record.get("decided_action")
        ok = got == exp_action
        checks.append({"name": f"decided_action=={exp_action}", "got": got, "passed": ok})

    # Check 2: tools_include (all named tools were called)
    for t in expected.get("tools_include", []):
        ok = t in tools_used
        checks.append({"name": f"tool_include:{t}", "passed": ok})

    # Check 3: tools_exclude (none of the named tools were called)
    for t in expected.get("tools_exclude", []):
        ok = t not in tools_used
        checks.append({"name": f"tool_exclude:{t}", "passed": ok})

    return {"checks": checks, "passed": all(c["passed"] for c in checks)}


def judge_semantic(client: anthropic.Anthropic, model: str, agent_output: str, criterion: str,
                   temperature: float = 0.0) -> dict:
    """LLM-as-judge: ask Claude if agent_output satisfies criterion."""
    # TODO: call client.messages.create with:
    #   model=model, max_tokens=512, temperature=temperature
    #   tools=[JUDGE_SCHEMA]
    #   tool_choice={"type":"tool","name":"submit_verdict"}
    #   messages=[{"role":"user","content": f"Criterion: {criterion}\n\nAgent output:\n{agent_output}\n\nDoes the agent output satisfy the criterion?"}]
    # Then find tool_use block, return dict(block.input) with keys passed, reasoning.
    #
    # HINT:
    #   response = client.messages.create(
    #       model=model, max_tokens=512,
    #       tools=[JUDGE_SCHEMA],
    #       tool_choice={"type": "tool", "name": "submit_verdict"},
    #       messages=[{"role": "user",
    #                  "content": f"Criterion: {criterion}\n\nAgent output:\n{agent_output}\n\nDoes the agent output satisfy the criterion? Answer via submit_verdict."}],
    #   )
    #   block = next(b for b in response.content if b.type == "tool_use")
    #   return dict(block.input)
    raise NotImplementedError("TODO: implement judge_semantic")


def score_case(client: anthropic.Anthropic, model: str, result: dict, expected: dict) -> dict:
    """Full scorecard for one eval case."""
    det = score_deterministic(result, expected)

    # Semantic criteria
    semantic_results = []
    agent_output = json.dumps({
        "action_record": result.get("action_record"),
        "tools_used": result.get("tools_used"),
        "audit_delta": result.get("audit_delta"),
    })
    for crit in expected.get("semantic_criteria", []):
        try:
            v = judge_semantic(client, model, agent_output, crit)
        except NotImplementedError as e:
            v = {"passed": False, "reasoning": f"judge_semantic TODO not filled: {e}"}
        semantic_results.append({"criterion": crit, **v})

    all_passed = det["passed"] and all(s["passed"] for s in semantic_results)
    return {"deterministic": det, "semantic": semantic_results, "all_passed": all_passed}
