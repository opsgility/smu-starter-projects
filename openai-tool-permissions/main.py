"""
Role-Based Tool Permission Sandbox
Course 201 - Lesson 8: Tool Permission Sandbox

Exercise: Build a role-based tool permission system where:
- admin:  can access all tools (read, write, delete, export)
- editor: can access read and write tools only
- viewer: can access read tools only

The model receives ONLY the tools allowed for the current role.
Tool invocations are blocked if the tool is not in the allowed set.

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically.
"""
from openai import OpenAI
from typing import Literal
import json

client = OpenAI()

# -----------------------------------------------------------------------
# Role definitions and permission mappings
# -----------------------------------------------------------------------

Role = Literal["admin", "editor", "viewer"]

ROLE_PERMISSIONS: dict[str, list[str]] = {
    "admin":  ["read_record", "write_record", "delete_record", "export_data"],
    "editor": ["read_record", "write_record"],
    "viewer": ["read_record"],
}

# -----------------------------------------------------------------------
# All available tools (full catalog)
# -----------------------------------------------------------------------

ALL_TOOLS = [
    {
        "type": "function",
        "name": "read_record",
        "description": "Read a customer record from the database by ID",
        "parameters": {
            "type": "object",
            "properties": {
                "record_id": {"type": "string", "description": "The customer record ID"}
            },
            "required": ["record_id"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "write_record",
        "description": "Create or update a customer record in the database",
        "parameters": {
            "type": "object",
            "properties": {
                "record_id": {"type": "string"},
                "data": {"type": "object", "description": "The record data to write"}
            },
            "required": ["record_id", "data"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "delete_record",
        "description": "Permanently delete a customer record from the database",
        "parameters": {
            "type": "object",
            "properties": {
                "record_id": {"type": "string"},
                "confirm": {"type": "boolean", "description": "Must be true to confirm deletion"}
            },
            "required": ["record_id", "confirm"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "export_data",
        "description": "Export all customer records to a CSV file",
        "parameters": {
            "type": "object",
            "properties": {
                "format": {"type": "string", "enum": ["csv", "json", "xlsx"]},
                "include_pii": {"type": "boolean", "description": "Include personally identifiable information"}
            },
            "required": ["format"],
            "additionalProperties": False
        },
        "strict": True
    }
]

# Tool name -> tool dict lookup
TOOL_REGISTRY = {tool["name"]: tool for tool in ALL_TOOLS}

# -----------------------------------------------------------------------
# Mock tool execution
# -----------------------------------------------------------------------

MOCK_DB = {
    "CUST-001": {"name": "Sarah Johnson", "email": "sarah@acme.com", "plan": "Enterprise"},
    "CUST-002": {"name": "Michael Chen", "email": "m.chen@medcore.io", "plan": "Pro"},
}


def execute_tool(tool_name: str, tool_args: dict) -> dict:
    """Execute a permitted tool and return mock result."""
    if tool_name == "read_record":
        record = MOCK_DB.get(tool_args["record_id"])
        return record if record else {"error": "Record not found"}
    elif tool_name == "write_record":
        MOCK_DB[tool_args["record_id"]] = tool_args["data"]
        return {"success": True, "record_id": tool_args["record_id"]}
    elif tool_name == "delete_record":
        if not tool_args.get("confirm"):
            return {"error": "Deletion requires confirm=true"}
        deleted = MOCK_DB.pop(tool_args["record_id"], None)
        return {"success": bool(deleted), "deleted": tool_args["record_id"]}
    elif tool_name == "export_data":
        return {"success": True, "records": len(MOCK_DB), "format": tool_args["format"]}
    return {"error": f"Unknown tool: {tool_name}"}


# -----------------------------------------------------------------------
# Exercises
# -----------------------------------------------------------------------

def get_allowed_tools(role: Role) -> list[dict]:
    """
    Exercise 1: Return only the tool schemas allowed for the given role.

    Use ROLE_PERMISSIONS to get the list of allowed tool names for the role.
    Filter ALL_TOOLS to only include tools whose name is in the allowed list.
    Return the filtered list of tool schemas.

    This filtered list is what gets sent to the model - the model can ONLY
    call tools it can see in its tool list.

    Args:
        role: "admin", "editor", or "viewer"

    Returns:
        List of tool schema dicts allowed for this role
    """
    allowed_names = ROLE_PERMISSIONS.get(role, [])
    # TODO: Filter ALL_TOOLS to only include tools whose "name" is in allowed_names
    # TODO: Return the filtered list
    return []


def permission_check(role: Role, tool_name: str) -> bool:
    """
    Exercise 2: Verify a role is allowed to call a specific tool.

    This is a server-side guard that runs BEFORE executing any tool.
    Even if the model somehow calls a tool not in its allowed set,
    this check prevents execution.

    Returns True if allowed, False if denied.

    Args:
        role: The current user's role
        tool_name: The tool the model is trying to call
    """
    # TODO: Check if tool_name is in ROLE_PERMISSIONS[role]
    # TODO: Return True if allowed, False if denied
    return False


def process_request(role: Role, user_request: str) -> str:
    """
    Exercise 3: Full permission-enforced tool execution.

    1. Get allowed tools for this role using get_allowed_tools()
    2. Send the request with ONLY the allowed tools
    3. If model calls a tool: run permission_check() before executing
       - If check passes: execute and continue
       - If check fails: log "PERMISSION DENIED" and stop
    4. Return the final assistant response

    This demonstrates defense-in-depth: the model only sees allowed tools
    (prevention), AND we verify server-side before execution (detection).

    Args:
        role: The current user's role
        user_request: The user's natural language request
    """
    allowed_tools = get_allowed_tools(role)
    print(f"\n[Role: {role.upper()}] Allowed tools: {[t['name'] for t in allowed_tools]}")
    print(f"Request: {user_request}")

    if not allowed_tools:
        return "No tools available for your role."

    # TODO: Call client.responses.create() with:
    #   model = "gpt-4.1-mini"
    #   input = user_request
    #   tools = allowed_tools
    #   tool_choice = "auto"

    # TODO: Check for tool calls in response.output
    # TODO: For each tool call:
    #   - Run permission_check(role, tool_call.name)
    #   - If denied: print "PERMISSION DENIED: {role} cannot call {tool_name}" and return
    #   - If allowed: execute_tool(tool_call.name, json.loads(tool_call.arguments))
    #   - Feed result back to model

    # TODO: Return final response.output_text
    return "Not implemented yet"


if __name__ == "__main__":
    test_cases = [
        ("admin",  "Read customer record CUST-001, then delete it"),
        ("editor", "Create a new record CUST-003 with name='Jamie Torres', email='j@test.com', plan='Pro'"),
        ("viewer", "Read record CUST-002 and show me the details"),
        ("viewer", "Delete record CUST-001"),      # Should be denied
        ("editor", "Export all data to CSV"),       # Should be denied
    ]

    print("Role-Based Tool Permission Demo")
    print("=" * 60)

    for role, request in test_cases:
        print()
        result = process_request(role, request)
        print(f"Result: {result}")
        print("-" * 40)
