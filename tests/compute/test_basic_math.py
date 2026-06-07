"""Test basic arithmetic operations."""
import pytest
from tests.compute import calculate_expression


def test_addition():
    assert calculate_expression("2 + 2") == 4


def test_subtraction():
    assert calculate_expression("10 - 3") == 7


def test_multiplication():
    assert calculate_expression("6 * 7") == 42


def test_division():
    assert calculate_expression("20 / 4") == 5


def test_parentheses():
    assert calculate_expression("(5 + 3) * 2") == 16


def test_decimal():
    assert calculate_expression("3.5 * 2") == 7.0
