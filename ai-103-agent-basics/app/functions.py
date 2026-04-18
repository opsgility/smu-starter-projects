"""Python functions exposed as agent tools.

Each function MUST have a complete docstring with parameter descriptions — the SDK
extracts those into the tool schema.
"""
import json


def get_weather(city: str) -> str:
    """Get the current weather for a city.

    :param city: The city name, e.g. "Seattle".
    :return: A JSON string with city, temp_f, and condition.
    """
    return json.dumps({"city": city, "temp_f": 72, "condition": "sunny"})


def calculate(expr: str) -> str:
    """Evaluate a basic arithmetic expression.

    :param expr: Expression like "12 * 3.5".
    :return: JSON string with the expression and the result.
    """
    import ast
    import operator as op

    ops = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv}

    def _eval(n):
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.BinOp):
            return ops[type(n.op)](_eval(n.left), _eval(n.right))
        raise ValueError("unsupported")

    return json.dumps({"expr": expr, "result": _eval(ast.parse(expr, mode="eval").body)})


_CATALOG = {"NW-001": 42, "NW-002": 7, "NW-003": 0}


def lookup_inventory(sku: str) -> str:
    """Look up stock for a Northwind product SKU.

    :param sku: SKU like "NW-001".
    :return: JSON string with sku and stock count.
    """
    return json.dumps({"sku": sku, "stock": _CATALOG.get(sku, 0)})


USER_FUNCTIONS = {get_weather, calculate, lookup_inventory}
