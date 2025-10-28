import math
import pytest
from app.operations import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5.0
    assert add(-1, 1.5) == 0.5

def test_subtract():
    assert subtract(5, 2) == 3.0
    assert subtract(2, 5) == -3.0

def test_multiply():
    assert multiply(2, 3) == 6.0
    assert multiply(-2, 3.5) == -7.0

def test_divide_normal():
    assert divide(10, 2) == 5.0
    assert math.isclose(divide(7, 3), 7/3)

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
