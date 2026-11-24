"""Test security protections against malicious input."""
import pytest
from tests.compute import calculate_expression


@pytest.mark.parametrize("payload", [
    "__import__('os')",
    "os.system('dir')",
    "eval('2+2')",
    "exec('print(1)')",
    "open('secret.txt')",
    "().__class__.__bases__",
    "import os; os.system('rm -rf /')",
    "[x for x in ().__class__.__bases__[0].__subclasses__() if x.__name__ == 'Popen']",
])
def test_malicious_input_rejected(payload):
    with pytest.raises(Exception):
        calculate_expression(payload)


def test_divide_by_zero():
    with pytest.raises(Exception):
        calculate_expression("5 / 0")


def test_empty_input():
    with pytest.raises(Exception):
        calculate_expression("")


def test_invalid_expression():
    with pytest.raises(Exception):
        calculate_expression("hello world")
