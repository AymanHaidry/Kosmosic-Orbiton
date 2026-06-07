"""Test mathematical constants."""
import pytest
import math
from tests.compute import calculate_expression


def test_pi():
    result = calculate_expression("pi")
    assert round(result, 5) == round(math.pi, 5)


def test_e():
    result = calculate_expression("e")
    assert round(result, 5) == round(math.e, 5)


def test_pi_in_expression():
    result = calculate_expression("pi * 2")
    assert round(result, 5) == round(math.pi * 2, 5)
