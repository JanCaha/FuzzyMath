import math
import pytest

from FuzzyMath.class_interval import Interval


def test_creation_errors():

    with pytest.raises(ArithmeticError,
                       match="`width` of interval must number higher or at least equal to 0."):
        Interval.midpoint_width(0, -1)

    with pytest.raises(ValueError,
                       match="The interval is invalid. `minimum` must be lower or equal to `maximum`"):
        Interval.infimum_supremum(3, 1)

    with pytest.raises(ValueError,
                       match="`precision` should be value from range `0` to `15`"):
        Interval(1, 3, precision=-1)
        Interval(1, 3, precision=16)

    with pytest.warns(UserWarning,
                      match="Using default value of precision"):
        Interval(1, 3, precision="pre")

    with pytest.raises(ValueError,
                       match="Cannot parse Interval from this definition"):
        Interval.parse_string("[1, 2.5, 5]")

    with pytest.raises(ValueError,
                       match="Cannot parse Interval from this definition"):
        Interval.parse_string("[]")

    with pytest.raises(ValueError,
                       match="Cannot parse Interval from this definition"):
        Interval.parse_string("[\"aa\", \"b\"]")


def test_creation():

    assert isinstance(Interval.infimum_supremum(1, 3), Interval)

    assert isinstance(Interval.infimum_supremum(2, 5), Interval)

    assert isinstance(Interval.infimum_supremum(4, 7), Interval)

    assert isinstance(Interval.infimum_supremum(-2, 3), Interval)

    assert isinstance(Interval.infimum_supremum(-1, 1), Interval)

    assert isinstance(Interval.empty(), Interval)

    interval = Interval.two_values(1.0000000000001, 3.000000009, precision=2)

    assert interval == Interval.two_values(1, 3, precision=2)

    interval = Interval.parse_string("[1, 2.5]")

    assert interval.min == 1
    assert interval.max == 2.5


def test_degenerate_interval():
    
    assert Interval.infimum_supremum(2, 2).degenerate
    assert Interval.infimum_supremum(2, 3).degenerate is False


def test_mid_point():
    
    a = Interval.two_values(1, 2)
    assert a.mid_point == 1.5

    b = Interval.midpoint_width(2, 2)
    assert b.mid_point == 2


def test_contains():

    interval = Interval.infimum_supremum(1, 5)

    assert 2 in interval
    assert 1 in interval
    assert 3.59 in interval

    assert (0.999999 in interval) is False
    assert (5.0001 in interval) is False

    print(Interval.two_values(6, 7) in interval)
    assert (Interval.two_values(6, 7) in interval) is False
    assert (Interval.two_values(0, 3) in interval) is False
    assert Interval.two_values(2, 4) in interval

    with pytest.raises(TypeError,
                       match="Cannot test if object of type "):
        "str" in interval
        True in interval


def test_intersects(i_a: Interval, i_b: Interval, i_c: Interval):

    assert i_a.intersects(i_b)
    assert i_b.intersects(i_a)
    assert i_b.intersects(i_c)
    assert i_c.intersects(i_b)

    assert i_a.intersects(i_c) is False
    assert i_c.intersects(i_a) is False


def test_intersection(i_a: Interval, i_b: Interval, i_c: Interval):
    
    assert i_a.intersection(i_b) == Interval.two_values(2, 3)
    assert i_b.intersection(i_c) == Interval.two_values(4, 5)
    
    with pytest.raises(ArithmeticError,
                       match="do not intersect"):
        i_a.intersection(i_c)


def test_union(i_a, i_b, i_c):
    
    assert i_a.union(i_b) == Interval.two_values(1, 5)
    assert i_b.union(i_c) == Interval.two_values(2, 7)

    with pytest.raises(ArithmeticError,
                       match="do not intersect"):
        i_a.union(i_c)


def test_union_hull(i_a: Interval, i_c: Interval):
    assert i_a.union_hull(i_c) == Interval.two_values(1, 7)


def test_add(i_a: Interval, i_b: Interval, i_e: Interval):
    
    assert i_a + 1 == Interval.two_values(i_a.min + 1, i_a.max + 1)
    
    assert 1 + i_a == Interval.two_values(i_a.min + 1, i_a.max + 1)
    
    assert i_a + i_b == Interval.two_values(i_a.min + i_b.min, i_a.max + i_b.max)
        
    assert i_a + i_e == Interval.two_values(i_a.min + i_e.min, i_a.max + i_e.max)

    with pytest.raises(TypeError,
                       match="unsupported operand"):
        i_a + "str"
        "str" + i_a


def test_sub(i_a: Interval, i_b: Interval):
    
    assert i_a - 1 == Interval.two_values(i_a.min - 1, i_a.max - 1)
    
    assert 1 - i_a == Interval.two_values(1 - i_a.min, 1 - i_a.max)
    
    assert i_a - i_b == Interval.two_values(i_a.min - i_b.max, i_a.max - i_b.min)
    
    with pytest.raises(TypeError,
                       match="unsupported operand"):
        i_a - "str"
        "str" - i_a


def test_mul(i_a: Interval, i_b: Interval):
    
    assert i_a * 2 == Interval.two_values(i_a.min * 2, i_a.max * 2)
    
    assert 2 * i_a == Interval.two_values(i_a.min * 2, i_a.max * 2)
    
    assert i_a * i_b == Interval.two_values(i_a.min * i_b.min, i_a.max * i_b.max)
    
    with pytest.raises(TypeError,
                       match="multiply sequence"):
        i_a * "str"
        "str" * i_a


def test_truediv(i_a: Interval, i_b: Interval, i_d: Interval):
    
    assert i_a / 2 == Interval.two_values(i_a.min / 2, i_a.max / 2)

    assert 2 / i_a == Interval.two_values(2 / i_a.min, 2 / i_a.max)
     
    assert i_a / i_b == Interval.two_values(i_a.min / i_b.max, i_a.max / i_b.min)
      
    with pytest.raises(TypeError,
                       match="unsupported operand"):
        i_a / "str"

    with pytest.raises(ArithmeticError,
                       match="Cannot divide by 0"):
        i_a / 0

    with pytest.raises(ArithmeticError,
                       match="Cannot divide by interval that contains `0`"):
        i_a / i_d


def test_pow(i_a: Interval, i_d: Interval):

    assert i_a ** 2 == Interval.two_values(1, 9)
    
    assert i_a ** 3 == Interval.two_values(1, 27)

    assert i_d ** 2 == Interval.two_values(0, 9)
    
    assert i_d ** 3 == Interval.two_values(-8, 27)


def test_neg(i_a: Interval, i_d: Interval):
    
    assert -i_a == Interval.two_values(i_a.min * (-1), i_a.max * (-1))
    
    assert -i_d == Interval.two_values(i_d.min * (-1), i_d.max * (-1))


def test_eq(i_a: Interval, i_b: Interval):
    
    assert i_a == i_a
    
    assert (i_a == i_b) is False


def test_lt(i_a: Interval, i_b: Interval, i_c: Interval, i_d: Interval):
    
    assert i_a < i_c
    
    assert i_d < i_c
    
    assert (i_a < i_b) is False
    
    
def test_gt(i_a: Interval, i_b: Interval, i_c: Interval, i_d: Interval):
    
    assert i_c > i_a
    
    assert i_c > i_d
    
    assert (i_b > i_a) is False
    
    
def test_lt_gt(i_a: Interval, i_b: Interval, i_c: Interval, i_d: Interval):
    
    assert (i_a < i_c) == (i_c > i_a)
    
    assert (i_d < i_c) == (i_c > i_d)
    
 
def test_is_empty(i_a: Interval, i_f: Interval):
     
    assert i_f.is_empty
    
    assert i_a.is_empty is False
    

def test_apply_function(i_a: Interval, i_b: Interval):

    # position argument not supported by the function
    with pytest.raises(TypeError,
                       match="too many positional arguments"):
        i_a.apply_function(math.log2, 5)

    # keyword argument that does not exist
    with pytest.raises(TypeError,
                       match="got an unexpected keyword argument 'c'"):
        i_a.apply_function(math.log2, c=5)

    assert i_a.apply_function(math.log2).min == pytest.approx(math.log2(i_a.min), 0.00001)
    
    assert i_a.apply_function(math.log2).max == pytest.approx(math.log2(i_a.max), 0.00001)
    
    assert i_b.apply_function(math.cos).min == pytest.approx(-1, 0.00001)
    
    assert i_b.apply_function(math.cos).max == pytest.approx(0.28366, 0.00001)
    
    assert i_a.apply_function(math.pow, 2, number_elements=10) == Interval.two_values(1, 9)
