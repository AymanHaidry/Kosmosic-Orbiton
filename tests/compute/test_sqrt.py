"""Test square root operations."""
import pytest
import math
from tests.compute import calculate_expression


def test_sqrt_16():
    assert calculate_expression("sqrt 16") == 4


def test_sqrt_144():
    assert calculate_expression("sqrt 144") == 12


def test_sqrt_2():
    assert round(calculate_expression("sqrt 2"), 5) == round(math.sqrt(2), 5)
