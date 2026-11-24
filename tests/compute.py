"""Compatibility helpers used by the legacy arithmetic test suite."""
import re

from stag.math_engine import MathNormalizer


def calculate_expression(expression):
    """Evaluate a spoken or symbolic arithmetic expression safely."""
    if not isinstance(expression, str):
        raise TypeError("Math expression must be text")
    normalized_input = expression.strip()
    normalized_input = re.sub(
        r"\bsqrt\s+(.+)$", r"square root of \1",
        normalized_input, flags=re.IGNORECASE,
    )
    normalized_input = re.sub(r"\be\b", "math.e", normalized_input)
    normalized = MathNormalizer.normalize(normalized_input)
    return MathNormalizer.safe_eval(normalized)
