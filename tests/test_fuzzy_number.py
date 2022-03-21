import pytest
import unittest
import math

from FuzzyMath.class_fuzzy_number import FuzzyNumber
from FuzzyMath.class_interval import Interval
from FuzzyMath.class_factories import FuzzyNumberFactory, IntervalFactory


def test_creation_errors():

    with pytest.raises(TypeError,
                       match="must be a list"):
        FuzzyNumber(1, [])

    with pytest.raises(TypeError,
                       match="must be a list"):
        FuzzyNumber([], 1)

    with pytest.raises(ValueError,
                       match="Lists `alphas` and `alpha_cuts` must be of same length."):
        FuzzyNumber([1, 2, 3], [1, 2])

    with pytest.raises(ValueError,
                       match="All elements of `alphas` must be from range"):
        FuzzyNumber([0, 0.5, 1, 1.1], [None] * 4)

    with pytest.raises(ValueError,
                       match="All elements of `alphas` must be int or float"):
        FuzzyNumber([0, 0.5, 1, "1.1"], [None] * 4)

    with pytest.raises(ValueError,
                       match="Values in `alphas` are not unique"):
        FuzzyNumber([0, 0.5, 1, 0.5], [None] * 4)

    with pytest.raises(ValueError,
                       match="`alphas` must contain both 0 and 1 alpha value"):
        FuzzyNumber([0, 0.5, 0.9], [None] * 3)

    with pytest.raises(ValueError,
                       match="`alphas` must contain both 0 and 1 alpha value"):
        FuzzyNumber([0.1, 0.5, 1], [None] * 3)

    with pytest.raises(TypeError,
                       match="All elements of `alpha_cuts` must be Interval"):
        FuzzyNumber([0, 1],
                    [IntervalFactory.two_values(0, 1), 5])

    with pytest.raises(ValueError,
                       match="Interval on lower alpha level has to contain the higher level alpha cuts"):
        FuzzyNumber([0, 1],
                    [IntervalFactory.two_values(0, 1),
                     IntervalFactory.two_values(2, 2)])

    with pytest.raises(ValueError,
                       match="The fuzzy number is invalid"):
        FuzzyNumberFactory.triangular(5, 4, 3)

    with pytest.raises(ValueError,
                       match="The fuzzy number is invalid"):
        FuzzyNumberFactory.trapezoidal(5, 1, 4, 3)


def test_creation():

    assert isinstance(FuzzyNumberFactory.triangular(1, 2, 3), FuzzyNumber)
    assert isinstance(FuzzyNumberFactory.triangular(1, 2, 3), FuzzyNumber)
    assert isinstance(FuzzyNumberFactory.triangular(1, 2, 3, number_of_cuts=10, precision=2), FuzzyNumber)

    assert isinstance(FuzzyNumberFactory.trapezoidal(1, 2, 3, 4), FuzzyNumber)
    assert isinstance(FuzzyNumberFactory.trapezoidal(1, 2, 3, 4, number_of_cuts=10, precision=2), FuzzyNumber)

    assert isinstance(FuzzyNumberFactory.crisp_number(0), FuzzyNumber)
    assert isinstance(FuzzyNumberFactory.crisp_number(0, precision=1), FuzzyNumber)


def test_fuzzynumber_creation_string():

    string_fn = '(0.0;1.0,3.0)(0.111111111111111;1.1,2.9)(0.222222222222222;1.2,2.8)(0.333333333333333;1.3,2.7)' \
        '(0.444444444444444;1.4,2.6)(0.555555555555556;1.5,2.5)(0.666666666666667;1.6,2.4)' \
        '(0.777777777777778;1.7,2.3)(0.888888888888889;1.8,2.2)(1.0;2.0,2.0)'

    assert isinstance(FuzzyNumberFactory.parse_string(string_fn), FuzzyNumber)

    string_fn = '(0.0;1,3)(0.5;1.9999,2.0001)(1.0;2,2)'

    assert isinstance(FuzzyNumberFactory.parse_string(string_fn), FuzzyNumber)

    assert isinstance(FuzzyNumberFactory.parse_string(string_fn, precision=1), FuzzyNumber)


def test_fuzzynumber_creation_string_errors():

    with pytest.raises(ValueError,
                       match="Cannot parse FuzzyNumber from this definition"):
        string_fn = '(0.0;1.0,3.0)(0.5;1.9999)(1.0;2.0,2.0)'
        FuzzyNumberFactory.parse_string(string_fn)

    with pytest.raises(ValueError,
                       match="element of Fuzzy Number"):
        string_fn = '(0.0;1.0,3.0)(0.5;2.0001,1.9999)(1.0;2.0,2.0)'
        FuzzyNumberFactory.parse_string(string_fn)

    with pytest.raises(ValueError,
                       match="element of Fuzzy Number"):
        string_fn = '(0.0;1.0,3.0)(1.1;1.9999,2.0001)(1.0;2.0,2.0)'
        FuzzyNumberFactory.parse_string(string_fn)

    with pytest.raises(ValueError,
                       match="Interval on lower alpha level has to contain the higher"):
        string_fn = '(0.0;1.0,3.0)(0.5;2.5,2.75)(1.0;2.0,2.0)'
        FuzzyNumberFactory.parse_string(string_fn)


def test_alphas(fn_a: FuzzyNumber, fn_e: FuzzyNumber):
    assert fn_a.alpha_levels == [0, 1]
    assert fn_e.alpha_levels == [0, 0.2, 0.4, 0.6, 0.8, 1]


def test_alpha_cuts(fn_a: FuzzyNumber):

    intervals = [IntervalFactory.infimum_supremum(1, 3),
                 IntervalFactory.infimum_supremum(2, 2)]

    assert intervals == fn_a.alpha_cuts


def test_get_alpha_cut(fn_a: FuzzyNumber):

    assert fn_a.get_alpha_cut(0) == IntervalFactory.two_values(1, 3)
    assert fn_a.get_alpha_cut(0.25) == IntervalFactory.two_values(1.25, 2.75)
    assert fn_a.get_alpha_cut(0.5) == IntervalFactory.two_values(1.5, 2.5)
    assert fn_a.get_alpha_cut(0.75) == IntervalFactory.two_values(1.75, 2.25)
    assert fn_a.get_alpha_cut(1) == IntervalFactory.two_values(2, 2)


def test_contain(fn_a: FuzzyNumber):

    assert 2 in fn_a
    assert 1 in fn_a
    assert 1.1 in fn_a
    assert 2.9 in fn_a
    assert 3 in fn_a
    assert IntervalFactory.infimum_supremum(2.9, 3.1) in fn_a
    assert FuzzyNumberFactory.crisp_number(3) in fn_a
    assert (0.999 in fn_a) is False
    assert (3.001 in fn_a) is False

    with pytest.raises(TypeError,
                       match="Cannot test if object of type"):
        "a" in fn_a


def test_get_alpha_cut_values():

    assert FuzzyNumber.get_alpha_cut_values(6, precision=4) == [0, 0.2, 0.4, 0.6, 0.8, 1]
    assert FuzzyNumber.get_alpha_cut_values(2, precision=4) == [0, 1]
    assert FuzzyNumber.get_alpha_cut_values(11, precision=8) == [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    with pytest.raises(ValueError,
                       match="`number_of_cuts` has to be integer and higher than 1"):
        FuzzyNumber.get_alpha_cut_values("str", precision=2)

    with pytest.raises(ValueError,
                       match="`number_of_cuts` has to be integer and higher than 1"):
        FuzzyNumber.get_alpha_cut_values(5.0, precision=2)

    with pytest.raises(ValueError,
                       match="`number_of_cuts` has to be integer and higher than 1"):
        FuzzyNumber.get_alpha_cut_values(1, precision=2)


def test_add(fn_a: FuzzyNumber, fn_b: FuzzyNumber, fn_c: FuzzyNumber):

    assert fn_a + 1 == FuzzyNumberFactory.triangular(2, 3, 4)

    assert 1 + fn_a == FuzzyNumberFactory.triangular(2, 3, 4)

    assert fn_a + fn_b == FuzzyNumberFactory.triangular(3, 5, 7)

    assert fn_b + fn_a == FuzzyNumberFactory.triangular(3, 5, 7)

    assert fn_a + fn_c == FuzzyNumberFactory.triangular(0, 2, 4)


def test_sub(fn_a: FuzzyNumber, fn_b: FuzzyNumber, fn_c: FuzzyNumber):

    assert fn_a - 1 == FuzzyNumberFactory.triangular(0, 1, 2)

    assert 1 - fn_a == FuzzyNumberFactory.triangular(-2, -1, 0)

    assert fn_a - fn_b == FuzzyNumberFactory.triangular(-3, -1, 1)

    assert fn_b - fn_a == FuzzyNumberFactory.triangular(-1, 1, 3)

    assert fn_a - fn_c == FuzzyNumberFactory.triangular(0, 2, 4)


def test_truediv(fn_a: FuzzyNumber, fn_b: FuzzyNumber, fn_c: FuzzyNumber):

    assert fn_a / 2 == FuzzyNumberFactory.triangular(0.5, 1, 1.5)

    with pytest.raises(ArithmeticError,
                       match="Cannot divide by 0"):
        fn_a / 0

    assert fn_a / fn_b == FuzzyNumberFactory.triangular(fn_a.min / fn_b.max,
                                                        fn_a.kernel.min / fn_b.kernel.min,
                                                        fn_a.max / fn_b.min)

    assert 5 / fn_a == FuzzyNumberFactory.triangular(5 / fn_a.max, 5 / fn_a.kernel.min, 5 / fn_a.min)


def test_pow(fn_a: FuzzyNumber):

    power = 2

    assert pow(fn_a, power) == FuzzyNumberFactory.triangular(1**power, 2**power, 3**power)


def test_function():

    fn = FuzzyNumberFactory.triangular(-math.pi / 2, 0, math.pi / 2, 11, 8)

    with pytest.raises(ValueError,
                       match="`function` must be either"):
        fn.apply_function(5)

    fn_cos = fn.apply_function(math.cos)

    diff = 0.00000001

    assert fn_cos.min == pytest.approx(-0, diff)
    assert fn_cos.max == pytest.approx(1, diff)
    assert fn_cos.kernel_min == pytest.approx(1, diff)

    fn_sin = fn.apply_function(math.sin)

    assert fn_sin.min == pytest.approx(-1, diff)
    assert fn_sin.max == pytest.approx(1, diff)
    assert fn_sin.kernel_min == pytest.approx(0, diff)


def test_comparisons(fn_a: FuzzyNumber, fn_b: FuzzyNumber, fn_c: FuzzyNumber):

    assert (fn_a == fn_b) is False
    assert fn_a == FuzzyNumberFactory.triangular(1, 2, 3)

    assert fn_c < fn_b
    assert (fn_c > fn_b) is False

    assert fn_c < 2
    assert (fn_c < -2) is False
    assert fn_c > -5
    assert(fn_c > 5) is False

    with pytest.raises(TypeError):
        fn_a > "test"


def test_complex_comparisons():

    fn_a = FuzzyNumberFactory.triangular(2, 3, 5)
    fn_b = FuzzyNumberFactory.triangular(1.5, 4, 4.8)

    diff = 0.000000001

    assert fn_a.possibility_exceedance(fn_b) == pytest.approx(0.7777777777777777, diff)

    assert fn_a.necessity_exceedance(fn_b) == pytest.approx(0.4285714285714289, diff)

    assert fn_a.possibility_strict_exceedance(fn_b) == pytest.approx(0.357142857142857, diff)

    assert fn_a.necessity_strict_exceedance(fn_b) == pytest.approx(0.0, diff)

    assert fn_a.possibility_undervaluation(fn_b) == pytest.approx(1.0, diff)

    assert fn_a.necessity_undervaluation(fn_b) == pytest.approx(0.6428571428571429, diff)

    assert fn_a.possibility_strict_undervaluation(fn_b) == pytest.approx(0.5714285714285711, diff)

    assert fn_a.necessity_strict_undervaluation(fn_b) == pytest.approx(0.22222222222222235, diff)

    fn_a = FuzzyNumberFactory.triangular(1.7, 2.7, 2.8)
    fn_b = FuzzyNumberFactory.triangular(0, 1.8, 2.2)

    assert fn_a.possibility_exceedance(fn_b) == pytest.approx(1.0, diff)

    assert fn_a.necessity_exceedance(fn_b) == pytest.approx(0.9642857142857143, diff)

    assert fn_a.possibility_strict_exceedance(fn_b) == pytest.approx(1.0, diff)

    assert fn_a.necessity_strict_exceedance(fn_b) == pytest.approx(0.642857142857143, diff)

    assert fn_a.possibility_undervaluation(fn_b) == pytest.approx(0.35714285714285726, diff)

    assert fn_a.necessity_undervaluation(fn_b) == pytest.approx(0.0, diff)

    assert fn_a.possibility_strict_undervaluation(fn_b) == pytest.approx(0.03571428571428574, diff)

    assert fn_a.necessity_strict_undervaluation(fn_b) == pytest.approx(0.0, diff)


def test_hash(i_a: FuzzyNumber):

    assert hash(i_a)

    assert isinstance(hash(i_a), int)


def test_repr(i_a: FuzzyNumber):

    assert isinstance(i_a.__repr__(), str)


def test_str(i_a: FuzzyNumber):

    assert isinstance(i_a.__str__(), str)
