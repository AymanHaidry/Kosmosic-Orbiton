"""Test square and cube operations."""
import pytest
from tests.compute import calculate_expression


def test_square():
    assert calculate_expression("5 squared") == 25


def test_squared():
    assert calculate_expression("5 squared") == 25


def test_cube():
    assert calculate_expression("3 cubed") == 27


def test_cubed():
    assert calculate_expression("4 cubed") == 64
