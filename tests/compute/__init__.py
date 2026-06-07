"""Shared compute test utilities."""
import re
import math


def calculate_expression(expr: str):
    """Mirror of CommandEngine.handle_calculate logic for testing."""
    safe_expr = expr.lower()
    safe_expr = re.sub(r"[^0-9+*/().^\s\squared\scubed\ssqrt\spi\se-]", "", safe_expr)
    safe_expr = safe_expr.replace("squared", "**2").replace("cubed", "**3")
    safe_expr = safe_expr.replace("times", "*").replace("x", "*")
    safe_expr = safe_expr.replace("divided by", "/")
    safe_expr = safe_expr.replace("pi", str(math.pi)).replace("e", str(math.e))
    safe_expr = safe_expr.replace("sqrt", "math.sqrt")
    # Handle natural language like "what is 25 times 4" -> extract numbers and ops
    if "what is" in safe_expr or "what's" in safe_expr:
        # Try to extract a simple arithmetic expression
        numbers = re.findall(r"\d+(?:\.\d+)?", safe_expr)
        if len(numbers) >= 2 and "times" in expr.lower():
            return float(numbers[0]) * float(numbers[1])
        if len(numbers) >= 2 and "percent of" in expr.lower():
            return float(numbers[0]) / 100 * float(numbers[1])
    if not safe_expr.strip():
        raise ValueError("Empty expression")
    result = eval(safe_expr, {"__builtins__": {}}, {"math": math})
    return result
