"""Test advanced mathematical operations."""
import pytest
import math
from tests.compute import calculate_expression


def test_exponents():
    assert calculate_expression("2 ** 10") == 1024


def test_modulus():
    assert calculate_expression("10 % 3") == 1


def test_power():
    assert calculate_expression("5 ** 2") == 25


def test_nested_parentheses():
    assert calculate_expression("((2 + 3) * 4) / 2") == 10.0
