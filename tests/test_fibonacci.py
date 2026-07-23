import pytest

from app.fibonacci import calculate_fibonacci


def test_fibonacci_zero():
    assert calculate_fibonacci(0) == 0


def test_fibonacci_one():
    assert calculate_fibonacci(1) == 1


def test_fibonacci_two():
    assert calculate_fibonacci(2) == 1


def test_fibonacci_ten():
    assert calculate_fibonacci(10) == 55


def test_fibonacci_twenty():
    assert calculate_fibonacci(20) == 6765


def test_fibonacci_thirty():
    assert calculate_fibonacci(30) == 832040


def test_negative_number():
    with pytest.raises(ValueError):
        calculate_fibonacci(-1)