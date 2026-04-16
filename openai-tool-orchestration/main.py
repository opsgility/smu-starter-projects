"""
Capstone Project: Production Tool Orchestration Runtime
Course 201 - Lesson 10: Capstone Project

Build a production-grade tool orchestration runtime with:
1. Tool registry with role-based access control (RBAC)
2. Parallel tool execution with timeout handling
3. Retry logic with exponential backoff on tool failure
4. All tool inputs/outputs validated against JSON Schema
5. Structured execution log (tool, args, result, latency, success/failure)

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
from typing import Literal, Optional
import json
import time
import concurrent.futures
import jsonschema
from datetime import datetime, timezone
from dataclasses import dataclass, asdict

client = OpenAI()

Role = Literal["admin", "editor", "viewer"]

# -----------------------------------------------------------------------
# Execution log entry
# -----------------------------------------------------------------------

@dataclass
class ExecutionLogEntry:
    timestamp: str
    tool_name: str
    role: str
    arguments: dict
    result: Optional[dict]
    latency_ms: float
    success: bool
    error: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self))


EXECUTION_LOG: list[ExecutionLogEntry] = []


# -----------------------------------------------------------------------
# Tool registry - each tool has: schema, handler, allowed_roles, output_schema
# -----------------------------------------------------------------------

def _handle_search(query: str, max_results: int = 5) -> dict:
    results = [
        {"title": f"Result {i} for '{query}'", "url": f"https://example.com/{i}", "snippet": f"...content about {query}..."}
        for i in range(1, min(max_results, 5) + 1)
    ]
    return {"query": query, "count": len(results), "results": results}

def _handle_send_email(to: str, subject: str, body: str) -> dict:
    return {"sent": True, "to": to, "subject": subject, "message_id": f"msg-{int(time.time())}"}

def _handle_update_record(record_id: str, updates: dict) -> dict:
    return {"updated": True, "record_id": record_id, "fields_updated": list(updates.keys())}

def _handle_delete_record(record_id: str, confirm: bool) -> dict:
    if not confirm:
        return {"deleted": False, "reason": "confirm must be true"}
    return {"deleted": True, "record_id": record_id}

def _handle_generate_report(report_type: str, date_range: str) -> dict:
    return {"report_type": report_type, "date_range": date_range, "records": 42, "generated_at": datetime.now(timezone.utc).isoformat()}


TOOL_REGISTRY = {
    "search": {
        "handler": _handle_search,
        "allowed_roles": ["admin", "editor", "viewer"],
        "schema": {
            "type": "function",
            "name": "search",
            "description": "Search for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "max_results": {"type": "integer", "default": 5}
                },
                "required": ["query"],
                "additionalProperties": False
            },
            "strict": True
        },
        "output_schema": {
            "type": "object",
            "required": ["query", "count", "results"],
            "properties": {
                "query": {"type": "string"},
                "count": {"type": "integer"},
                "results": {"type": "array"}
            }
        }
    },
    "send_email": {
        "handler": _handle_send_email,
        "allowed_roles": ["admin", "editor"],
        "schema": {
            "type": "function",
            "name": "send_email",
            "description": "Send an email",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"}
                },
                "required": ["to", "subject", "body"],
                "additionalProperties": False
            },
            "strict": True
        },
        "output_schema": {
            "type": "object",
            "required": ["sent", "to"],
            "properties": {"sent": {"type": "boolean"}, "to": {"type": "string"}}
        }
    },
    "update_record": {
        "handler": _handle_update_record,
        "allowed_roles": ["admin", "editor"],
        "schema": {
            "type": "function",
            "name": "update_record",
            "description": "Update a database record",
            "parameters": {
                "type": "object",
                "properties": {
                    "record_id": {"type": "string"},
                    "updates": {"type": "object"}
                },
                "required": ["record_id", "updates"],
                "additionalProperties": False
            },
            "strict": True
        },
        "output_schema": {
            "type": "object",
            "required": ["updated", "record_id"],
            "properties": {"updated": {"type": "boolean"}, "record_id": {"type": "string"}}
        }
    },
    "delete_record": {
        "handler": _handle_delete_record,
        "allowed_roles": ["admin"],
        "schema": {
            "type": "function",
            "name": "delete_record",
            "description": "Delete a database record",
            "parameters": {
                "type": "object",
                "properties": {
                    "record_id": {"type": "string"},
                    "confirm": {"type": "boolean"}
                },
                "required": ["record_id", "confirm"],
                "additionalProperties": False
            },
            "strict": True
        },
        "output_schema": {
            "type": "object",
            "required": ["deleted"],
            "properties": {"deleted": {"type": "boolean"}}
        }
    },
    "generate_report": {
        "handler": _handle_generate_report,
        "allowed_roles": ["admin"],
        "schema": {
            "type": "function",
            "name": "generate_report",
            "description": "Generate a business intelligence report",
            "parameters": {
                "type": "object",
                "properties": {
                    "report_type": {"type": "string", "enum": ["sales", "usage", "billing", "performance"]},
                    "date_range": {"type": "string", "description": "e.g. 'Q1 2026' or 'March 2026'"}
                },
                "required": ["report_type", "date_range"],
                "additionalProperties": False
            },
            "strict": True
        },
        "output_schema": {
            "type": "object",
            "required": ["report_type", "date_range", "records"],
            "properties": {
                "report_type": {"type": "string"},
                "date_range": {"type": "string"},
                "records": {"type": "integer"}
            }
        }
    }
}


def get_tools_for_role(role: Role) -> list[dict]:
    """Exercise 1: Return tool schemas for tools allowed for the given role."""
    # TODO: Filter TOOL_REGISTRY to tools where role is in tool["allowed_roles"]
    # TODO: Return list of tool["schema"] for each allowed tool
    return []


def validate_output(tool_name: str, output: dict) -> bool:
    """Exercise 4: Validate tool output against its JSON Schema using jsonschema."""
    tool = TOOL_REGISTRY.get(tool_name)
    if not tool:
        return False
    # TODO: Use jsonschema.validate(output, tool["output_schema"])
    # TODO: Return True if valid, False if jsonschema.ValidationError is raised
    return True


def execute_with_retry(tool_name: str, args: dict, role: Role,
                       max_retries: int = 3, timeout_sec: float = 10.0) -> ExecutionLogEntry:
    """
    Exercise 2 & 3: Execute a tool with timeout and exponential backoff.

    1. Check role permission
    2. Execute the tool handler in a ThreadPoolExecutor with timeout
    3. On failure: wait 2^attempt seconds and retry (up to max_retries)
    4. Validate output schema
    5. Log the result as ExecutionLogEntry

    Returns an ExecutionLogEntry whether success or failure.
    """
    start = time.time()

    # Permission check
    tool_info = TOOL_REGISTRY.get(tool_name)
    if not tool_info or role not in tool_info["allowed_roles"]:
        entry = ExecutionLogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            tool_name=tool_name, role=role, arguments=args, result=None,
            latency_ms=0, success=False, error=f"Permission denied for role '{role}'"
        )
        EXECUTION_LOG.append(entry)
        return entry

    result = None
    error = None

    for attempt in range(max_retries):
        try:
            # TODO: Use concurrent.futures.ThreadPoolExecutor to run
            #       tool_info["handler"](**args) with a timeout of timeout_sec seconds
            # TODO: On concurrent.futures.TimeoutError: set error, retry with backoff
            # TODO: On success: break out of retry loop
            pass
        except Exception as e:
            error = str(e)
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"  Tool '{tool_name}' failed (attempt {attempt+1}): {e}. Retrying in {wait}s...")
                time.sleep(wait)

    latency_ms = (time.time() - start) * 1000
    success = result is not None

    # Validate output schema if successful
    if success and not validate_output(tool_name, result):
        success = False
        error = "Output schema validation failed"

    entry = ExecutionLogEntry(
        timestamp=datetime.now(timezone.utc).isoformat(),
        tool_name=tool_name, role=role, arguments=args,
        result=result, latency_ms=round(latency_ms, 2),
        success=success, error=error
    )
    EXECUTION_LOG.append(entry)
    return entry


def run_orchestration(role: Role, user_request: str) -> str:
    """
    Exercise 5: Full orchestration pipeline.

    1. Get tools for role
    2. Call model with available tools
    3. For each tool call: execute_with_retry()
    4. Feed results back to model
    5. Return final response
    """
    print(f"\n[{role.upper()}] {user_request}")
    allowed_tools = get_tools_for_role(role)
    print(f"  Available tools: {[t['name'] for t in allowed_tools]}")

    # TODO: Call client.responses.create() with allowed tools
    # TODO: Process tool calls with execute_with_retry()
    # TODO: Feed results back and get final answer
    # TODO: Return final response.output_text
    return "Not implemented yet"


def print_execution_log() -> None:
    """Print the execution log for all tool invocations."""
    print("\n" + "=" * 60)
    print("EXECUTION LOG")
    print("=" * 60)
    for entry in EXECUTION_LOG:
        status = "✓" if entry.success else "✗"
        print(f"  {status} {entry.tool_name} | {entry.role} | {entry.latency_ms:.0f}ms | {entry.error or 'OK'}")


if __name__ == "__main__":
    print("Production Tool Orchestration Runtime")
    print("=" * 60)

    scenarios = [
        ("admin",  "Search for AI trends, then generate a performance report for Q1 2026"),
        ("editor", "Search for 'customer churn' and send an email to team@company.com with a summary"),
        ("viewer", "Search for information about our pricing plans"),
        ("viewer", "Delete record CUST-001"),  # Should be denied
        ("editor", "Generate a sales report for March 2026"),  # Should be denied
    ]

    for role, request in scenarios:
        result = run_orchestration(role, request)
        print(f"  Response: {result[:100] if result else 'N/A'}")

    print_execution_log()
