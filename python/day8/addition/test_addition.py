from addition import add, divide
from addition import subtract, multiply

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5 #True

def test_add_zero():
    assert add(0, 5) == 5

def test_add_positive_and_negative():
    assert add(5, -3) == 2

def test_add_floats():
    assert add(2.5, 3.1) == 5.6

#two testcases for subtraction 
def test_substract():
    assert subtract(5, 3) == 2

def test_subtract_negative_numbers():
    assert subtract(-5, -3) == -2

def test_multiply_zero():
    assert multiply(5, 0) == 0

#two testcases for divide function
def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    try:
        divide(10, 0)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError when dividing by zero"