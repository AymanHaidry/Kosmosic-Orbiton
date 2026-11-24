"""Shared compute test utilities."""
import re
import math


def calculate_expression(expr: str):
    """Mirror of CommandEngine.handle_calculate logic for testing."""
    safe_expr = expr.lower()
    safe_expr = re.sub(r"[^0-9+*/().^\s\squared\scubed\ssqrt\spi\se%-]", "", safe_expr)
    safe_expr = safe_expr.replace("squared", "**2").replace("cubed", "**3")
    safe_expr = safe_expr.replace("times", "*").replace("x", "*")
    safe_expr = safe_expr.replace("divided by", "/")
    safe_expr = safe_expr.replace("pi", str(math.pi)).replace("e", str(math.e))
    # Handle sqrt with parentheses if not present
    safe_expr = re.sub(r"sqrt\s+(\d+(?:\.\d+)?)", r"math.sqrt(\1)", safe_expr)
    if not safe_expr.strip():
        raise ValueError("Empty expression")
    result = eval(safe_expr, {"__builtins__": {}}, {"math": math})
    return result
