"""
Neuro-Link Compute Engine Tests

Covers:
- Basic arithmetic
- Advanced math
- Constants
- Square/Cube operations
- Square roots
- Security
"""

import math
import pytest

from neuro_link import calculate_expression


# ============================================================
# BASIC MATH
# ============================================================

def test_addition():
    assert calculate_expression("2+2") == 4


def test_subtraction():
    assert calculate_expression("10-3") == 7


def test_multiplication():
    assert calculate_expression("6*7") == 42


def test_division():
    assert calculate_expression("20/4") == 5


def test_parentheses():
    assert calculate_expression("(5+3)*2") == 16


# ============================================================
# ADVANCED MATH
# ============================================================

def test_exponents():
    assert calculate_expression("2**10") == 1024


def test_modulus():
    assert calculate_expression("10%3") == 1


def test_factorial():
    assert calculate_expression("factorial 5") == 120


# ============================================================
# CONSTANTS
# ============================================================

def test_pi():
    result = calculate_expression("pi")
    assert round(result, 5) == round(math.pi, 5)


def test_e():
    result = calculate_expression("e")
    assert round(result, 5) == round(math.e, 5)


# ============================================================
# SQUARE / CUBE
# ============================================================

def test_square():
    assert calculate_expression("square 5") == 25


def test_squared():
    assert calculate_expression("5 squared") == 25


def test_cube():
    assert calculate_expression("cube 3") == 27


def test_cubed():
    assert calculate_expression("4 cubed") == 64


# ============================================================
# SQRT
# ============================================================

def test_sqrt_16():
    assert calculate_expression("sqrt 16") == 4


def test_sqrt_144():
    assert calculate_expression("sqrt 144") == 12


def test_sqrt_2():
    assert round(
        calculate_expression("sqrt 2"),
        5
    ) == round(math.sqrt(2), 5)


# ============================================================
# NATURAL LANGUAGE
# ============================================================

def test_natural_language_multiply():
    assert calculate_expression(
        "what is 25 times 4"
    ) == 100


def test_natural_language_percent():
    assert calculate_expression(
        "50 percent of 800"
    ) == 400


# ============================================================
# SECURITY
# ============================================================

@pytest.mark.parametrize(
    "payload",
    [
        "__import__('os')",
        "os.system('dir')",
        "eval('2+2')",
        "exec('print(1)')",
        "open('secret.txt')",
        "().__class__.__bases__",
    ],
)
def test_malicious_input_rejected(payload):
    with pytest.raises(Exception):
        calculate_expression(payload)


# ============================================================
# EDGE CASES
# ============================================================

def test_divide_by_zero():
    with pytest.raises(Exception):
        calculate_expression("5/0")


def test_empty_input():
    with pytest.raises(Exception):
        calculate_expression("")


def test_invalid_expression():
    with pytest.raises(Exception):
        calculate_expression("hello world")
