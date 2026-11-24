"""Regression tests for spoken math normalization and safe evaluation."""
import math
import pytest
from neuro_link_intel import MathNormalizer

@pytest.mark.parametrize(("spoken","expected"),[
 ("two times two","2*2"),("twenty five divided by five","25/5"),
 ("one hundred twenty five minus twenty","125-20"),("three squared","3**2"),
 ("three to the power of four","3**4"),("fifty percent of two hundred","50/100*200"),
 ("square root of nine","math.sqrt(9)"),("cube root of twenty seven","math.cbrt(27)"),
 ("factorial of five","math.factorial(5)"),
])
def test_normalize_spoken_math(spoken,expected):
 assert MathNormalizer.normalize(spoken)==expected

@pytest.mark.parametrize(("expr","expected"),[
 ("2+3*4",14),("(2+3)*4",20),("25/5",5),("3**4",81),
 ("math.sqrt(81)",9),("math.cbrt(27)",3),("math.factorial(5)",120),
 ("round(3.14159,2)",3.14),("abs(-7)",7),
])
def test_safe_eval_arithmetic(expr,expected):
 assert MathNormalizer.safe_eval(expr)==pytest.approx(expected)

def test_safe_eval_math_constants():
 assert MathNormalizer.safe_eval("math.pi")==math.pi
 assert MathNormalizer.safe_eval("math.e")==math.e

@pytest.mark.parametrize("expr",[
 "", "__import__('os').system('echo unsafe')", "open('/tmp/x','w')",
 "math.__dict__", "round.__class__", "2**101", "1/0", "True+1",
])
def test_safe_eval_rejects_unsafe_expressions(expr):
 with pytest.raises(ValueError): MathNormalizer.safe_eval(expr)

def test_safe_eval_rejects_long_input():
 with pytest.raises(ValueError,match="too long"): MathNormalizer.safe_eval("1"*257)
