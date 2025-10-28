from typing import Union

Number = Union[int, float]

def add(a: Number, b: Number) -> float:
    return float(a) + float(b)

def subtract(a: Number, b: Number) -> float:
    return float(a) - float(b)

def multiply(a: Number, b: Number) -> float:
    return float(a) * float(b)

def divide(a: Number, b: Number) -> float:
    if float(b) == 0:
        raise ZeroDivisionError("Division by zero")
    return float(a) / float(b)
