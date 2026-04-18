"""Tool definitions + Python implementations for the chat agent."""
from __future__ import annotations

import ast
import operator as op

# Tool schemas — sent to the model as `tools=[...]` on every request.
TOOL_SCHEMAS: list[dict] = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Return the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
    {
        "type": "function",
        "name": "calculate",
        "description": "Evaluate a basic arithmetic expression safely.",
        "parameters": {
            "type": "object",
            "properties": {"expr": {"type": "string"}},
            "required": ["expr"],
        },
    },
    {
        "type": "function",
        "name": "lookup_inventory",
        "description": "Look up stock for a Northwind product SKU.",
        "parameters": {
            "type": "object",
            "properties": {"sku": {"type": "string"}},
            "required": ["sku"],
        },
    },
]

_CATALOG = {"NW-001": 42, "NW-002": 7, "NW-003": 0}
_BIN_OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Mod: op.mod, ast.Pow: op.pow}


def get_weather(city: str) -> dict:
    # Simple deterministic mock so tests are reproducible.
    return {"city": city, "temp_f": 72, "condition": "sunny"}


def calculate(expr: str) -> dict:
    node = ast.parse(expr, mode="eval").body

    def _eval(n: ast.AST) -> float:
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in _BIN_OPS:
            return _BIN_OPS[type(n.op)](_eval(n.left), _eval(n.right))
        raise ValueError(f"Unsupported expression: {ast.dump(n)}")

    return {"expr": expr, "result": _eval(node)}


def lookup_inventory(sku: str) -> dict:
    return {"sku": sku, "stock": _CATALOG.get(sku, 0)}


DISPATCH = {
    "get_weather": get_weather,
    "calculate": calculate,
    "lookup_inventory": lookup_inventory,
}
