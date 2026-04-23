"""
Capstone Project: Tool Orchestration Runtime
Course 201 - Lesson 10: Capstone Project

Build a production-grade tool orchestration runtime with:
1. Tool registry with role-based access control
2. Parallel tool execution with timeout handling
3. Retry logic with exponential backoff on tool failure
4. JSON Schema validation of all tool inputs/outputs
5. Structured execution log (tool name, args, result, latency, success)

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
from pydantic import BaseModel
import json
import time

client = OpenAI()


class ToolExecution(BaseModel):
    tool_name: str
    arguments: dict
    result: str
    latency_ms: float
    success: bool
    attempts: int
    role: str


TOOL_REGISTRY = {
    "get_weather": {
        "schema": {
            "type": "function",
            "name": "get_weather",
            "description": "Get current weather for a location.",
            "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"],
                "additionalProperties": False,
            },
            "strict": True,
        },
        "roles": ["viewer", "editor", "admin"],
        "output_schema": {
            "type": "object",
            "required": ["location", "temperature", "condition"],
            "properties": {
                "location": {"type": "string"},
                "temperature": {"type": "string"},
                "condition": {"type": "string"},
            },
        },
    },
    "write_report": {
        "schema": {
            "type": "function",
            "name": "write_report",
            "description": "Write a report to the data store.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["title", "content"],
                "additionalProperties": False,
            },
            "strict": True,
        },
        "roles": ["editor", "admin"],
        "output_schema": {
            "type": "object",
            "required": ["status", "report_id"],
            "properties": {
                "status": {"type": "string"},
                "report_id": {"type": "string"},
            },
        },
    },
    "delete_report": {
        "schema": {
            "type": "function",
            "name": "delete_report",
            "description": "Delete a report by ID.",
            "parameters": {
                "type": "object",
                "properties": {"report_id": {"type": "string"}},
                "required": ["report_id"],
                "additionalProperties": False,
            },
            "strict": True,
        },
        "roles": ["admin"],
        "output_schema": {
            "type": "object",
            "required": ["status"],
            "properties": {"status": {"type": "string"}},
        },
    },
}

_fail_counter = {}


def get_weather(location: str) -> dict:
    """Simulates transient failures to test retry logic."""
    _fail_counter["get_weather"] = _fail_counter.get("get_weather", 0) + 1
    if _fail_counter["get_weather"] % 3 == 1:  # Fail every 1st call, succeed on retry
        raise RuntimeError("Weather API timeout")
    return {"location": location, "temperature": "72F", "condition": "Sunny"}


def write_report(title: str, content: str) -> dict:
    report_id = f"RPT-{int(time.time() * 1000) % 100000}"
    return {"status": "written", "report_id": report_id}


def delete_report(report_id: str) -> dict:
    return {"status": "deleted"}


TOOL_IMPLEMENTATIONS = {
    "get_weather": get_weather,
    "write_report": write_report,
    "delete_report": delete_report,
}


def validate_output(tool_name: str, output: dict) -> bool:
    """
    Exercise 1: Validate tool output against its registered output schema.

    Check all required fields are present in output.
    For each required field, check isinstance(output[field], expected_type)
    where "string" -> str, "integer" -> int, "number" -> float.
    Return True if all checks pass, False otherwise.
    """
    registry_entry = TOOL_REGISTRY.get(tool_name)
    if not registry_entry:
        return False
    schema = registry_entry["output_schema"]

    # TODO: Get the list of required field names from schema["required"]
    # TODO: For each required field, check it exists in output
    # TODO: Check type: schema["properties"][field]["type"] -> map to Python type
    # TODO: Return True only if all fields present and correctly typed
    pass


def execute_tool_with_retry(tool_name: str, arguments: dict, role: str,
                              max_retries: int = 3) -> ToolExecution:
    """
    Exercise 2: Execute a tool with permission check, retry, and logging.

    Steps:
    1. Check role is in TOOL_REGISTRY[tool_name]["roles"] - return failure if not
    2. Try calling TOOL_IMPLEMENTATIONS[tool_name](**arguments)
    3. On exception: sleep(2**attempt) and retry up to max_retries
    4. On success: validate output, return ToolExecution(success=True)
    5. After all retries fail: return ToolExecution(success=False)
    """
    start = time.time()
    allowed_roles = TOOL_REGISTRY.get(tool_name, {}).get("roles", [])

    if role not in allowed_roles:
        return ToolExecution(
            tool_name=tool_name, arguments=arguments,
            result=json.dumps({"error": f"Role '{role}' cannot call '{tool_name}'"}),
            latency_ms=0.0, success=False, attempts=0, role=role,
        )

    impl = TOOL_IMPLEMENTATIONS.get(tool_name)
    if not impl:
        return ToolExecution(
            tool_name=tool_name, arguments=arguments,
            result=json.dumps({"error": "Tool not implemented"}),
            latency_ms=0.0, success=False, attempts=0, role=role,
        )

    # TODO: for attempt in range(max_retries):
    # TODO:     try:
    # TODO:         result = impl(**arguments)
    # TODO:         valid = validate_output(tool_name, result)
    # TODO:         latency = (time.time() - start) * 1000
    # TODO:         return ToolExecution(success=True, attempts=attempt+1,
    #                                    result=json.dumps(result), latency_ms=latency, ...)
    # TODO:     except Exception:
    # TODO:         if attempt < max_retries - 1:
    # TODO:             time.sleep(2 ** attempt)
    # TODO: return ToolExecution(success=False, attempts=max_retries, ...)
    pass


def run_orchestration(user_query: str, role: str) -> tuple:
    """
    Exercise 3: Full orchestration loop with execution logging.

    Steps:
    1. Build tool list from TOOL_REGISTRY filtered by role
    2. Call client.responses.create(model="gpt-4.1-mini", input=[...], tools=tools)
    3. For each function_call in response.output:
       - Parse arguments as JSON
       - Call execute_tool_with_retry(name, args, role)
       - Append ToolExecution to execution_log
    4. Build tool_result messages and make follow-up call
    5. Return (response.output_text, execution_log)
    """
    print(f"\n[{role.upper()}] {user_query}")
    execution_log: list[ToolExecution] = []

    tools = [
        entry["schema"]
        for name, entry in TOOL_REGISTRY.items()
        if role in entry["roles"]
    ]
    print(f"  Available tools: {[t['name'] for t in tools]}")

    # TODO: Call client.responses.create() with user_query and tools
    # TODO: Collect all function_call items from response.output
    # TODO: Execute each using execute_tool_with_retry, append to execution_log
    # TODO: Feed tool results back as function_call_output items:
    #       {"type": "function_call_output", "call_id": call.call_id, "output": execution.result}
    #       NOTE: use call.call_id (e.g. "call_..."), NOT call.id (e.g. "fc_...").
    # TODO: Return (output_text, execution_log)
    pass


def print_execution_log(log: list) -> None:
    if not log:
        return
    print("\n  EXECUTION LOG:")
    for entry in log:
        status = "OK" if entry.success else "FAIL"
        print(f"    [{status}] {entry.tool_name} | {entry.latency_ms:.0f}ms | {entry.attempts} attempt(s)")
        if not entry.success:
            data = json.loads(entry.result)
            print(f"          {data.get('error', 'Unknown error')}")


if __name__ == "__main__":
    print("Tool Orchestration Runtime — Course 201 Capstone")
    print("=" * 55)

    scenarios = [
        ("Get the weather in Seattle, then write a brief weather report.", "editor"),
        ("What is the weather in Tokyo?", "viewer"),
        ("Delete report RPT-12345.", "viewer"),
        ("Get weather in Paris and write a summary report.", "admin"),
    ]

    for query, role in scenarios:
        result, log = run_orchestration(query, role)
        if result:
            print(f"  Response: {result}")
        print_execution_log(log)
