"""
Tool Permission Sandbox
Course 201 - Lesson 8: Tool Permission Boundaries & Output Verification

Role-based tool permission system where admin, editor, and viewer roles
each have different tool access. The model can only invoke tools allowed
for the current role.

IMPORTANT: OPENAI_API_KEY and OPENAI_BASE_URL are pre-configured in your
environment automatically. Do NOT set them manually.
"""
from openai import OpenAI
import json

client = OpenAI()

# ---- All available tools ----

ALL_TOOLS = [
    {
        "type": "function",
        "name": "read_document",
        "description": "Read the contents of a document by name.",
        "parameters": {
            "type": "object",
            "properties": {
                "document_name": {"type": "string", "description": "Name of the document to read"},
            },
            "required": ["document_name"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "write_document",
        "description": "Write or update content in a document.",
        "parameters": {
            "type": "object",
            "properties": {
                "document_name": {"type": "string"},
                "content": {"type": "string", "description": "New content to write"},
            },
            "required": ["document_name", "content"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "delete_document",
        "description": "Permanently delete a document.",
        "parameters": {
            "type": "object",
            "properties": {
                "document_name": {"type": "string"},
            },
            "required": ["document_name"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "list_users",
        "description": "List all users in the system (admin only).",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "promote_user",
        "description": "Promote a user to a higher role (admin only).",
        "parameters": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "new_role": {"type": "string", "enum": ["viewer", "editor", "admin"]},
            },
            "required": ["username", "new_role"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

# ---- Role → allowed tool names ----
# viewer:  read only
# editor:  read + write
# admin:   all tools

ROLE_PERMISSIONS = {
    "viewer": {"read_document"},
    "editor": {"read_document", "write_document"},
    "admin":  {"read_document", "write_document", "delete_document", "list_users", "promote_user"},
}


def get_tools_for_role(role: str) -> list:
    """
    Exercise 1: Return only the tool schemas allowed for the given role.

    Filter ALL_TOOLS to those whose "name" is in ROLE_PERMISSIONS[role].
    If the role is unknown, return an empty list.

    Returns:
        list of tool schema dicts
    """
    # TODO: Look up allowed tool names from ROLE_PERMISSIONS
    # TODO: Filter ALL_TOOLS to only those whose name is in the allowed set
    # TODO: Return the filtered list
    pass


# ---- Simulated tool implementations ----

DOCUMENT_STORE = {
    "report_q1.txt":   "Q1 2026 Revenue: $3.2M. Net ARR: $1.8M.",
    "team_roster.txt": "Alice (admin), Bob (editor), Carol (viewer).",
    "roadmap.txt":     "Q2: Launch v2. Q3: Enterprise tier. Q4: IPO prep.",
}

USER_DB = {
    "alice": "admin",
    "bob":   "editor",
    "carol": "viewer",
}


def execute_tool(name: str, arguments: dict, role: str) -> str:
    """
    Execute a tool — but first verify the calling role has permission.
    Returns JSON result string or permission denied message.
    """
    allowed = ROLE_PERMISSIONS.get(role, set())
    if name not in allowed:
        return json.dumps({"error": f"Permission denied: role '{role}' cannot call '{name}'"})

    if name == "read_document":
        content = DOCUMENT_STORE.get(arguments["document_name"], "Document not found.")
        return json.dumps({"document": arguments["document_name"], "content": content})

    elif name == "write_document":
        DOCUMENT_STORE[arguments["document_name"]] = arguments["content"]
        return json.dumps({"status": "written", "document": arguments["document_name"]})

    elif name == "delete_document":
        deleted = DOCUMENT_STORE.pop(arguments["document_name"], None)
        return json.dumps({"status": "deleted" if deleted else "not_found"})

    elif name == "list_users":
        return json.dumps({"users": USER_DB})

    elif name == "promote_user":
        USER_DB[arguments["username"]] = arguments["new_role"]
        return json.dumps({"status": "promoted", "user": arguments["username"], "role": arguments["new_role"]})

    return json.dumps({"error": "Unknown tool"})


def run_with_role(user_query: str, role: str) -> str:
    """
    Exercise 2: Run the assistant with role-based tool access.

    Steps:
    1. Call get_tools_for_role(role) to get the allowed tool subset
    2. Send the query to the model with only the allowed tools
    3. Handle any tool calls (use execute_tool with the role for permission check)
    4. Return the final response

    Use client.responses.create() with model="gpt-4.1-mini".
    """
    print(f"\n[{role.upper()}] Query: {user_query}")
    tools = get_tools_for_role(role)
    print(f"  Tools available: {[t['name'] for t in tools]}")

    # TODO: Call client.responses.create() with the filtered tools
    # TODO: Handle any function calls using execute_tool(name, args, role)
    # TODO: Make follow-up call with tool results
    # TODO: Return final response text
    pass


if __name__ == "__main__":
    print("Tool Permission Sandbox — Course 201 Lesson 8")
    print("=" * 50)

    # Test all three roles with the same queries
    queries = [
        ("Read report_q1.txt and summarize it.", "viewer"),
        ("Read report_q1.txt and then update roadmap.txt with 'Q2: Ship v2'.", "editor"),
        ("List all users and then promote carol to editor.", "admin"),
        ("Delete report_q1.txt.", "viewer"),   # Should be denied
    ]

    for query, role in queries:
        result = run_with_role(query, role)
        if result:
            print(f"  Response: {result}\n")
