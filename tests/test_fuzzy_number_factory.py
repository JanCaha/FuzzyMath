from decimal import Decimal

import pytest

from FuzzyMath.class_factories import FuzzyNumberFactory, IntervalFactory
from FuzzyMath.class_fuzzy_number import FuzzyNumber


def test_creation_errors():
    with pytest.raises(ValueError, match="The fuzzy number is invalid"):
        FuzzyNumberFactory.triangular(5, 4, 3)

    with pytest.raises(ValueError, match="The fuzzy number is invalid"):
        FuzzyNumberFactory.trapezoidal(5, 1, 4, 3)


def test_creation():
    assert isinstance(FuzzyNumberFactory.triangular(1, 2, 3), FuzzyNumber)
    assert isinstance(FuzzyNumberFactory.triangular(1, 2, 3), FuzzyNumber)
    assert isinstance(FuzzyNumberFactory.triangular(1, 2, 3, number_of_cuts=10), FuzzyNumber)

    assert isinstance(FuzzyNumberFactory.trapezoidal(1, 2, 3, 4), FuzzyNumber)
    assert isinstance(FuzzyNumberFactory.trapezoidal(1, 2, 3, 4, number_of_cuts=10), FuzzyNumber)

    assert isinstance(FuzzyNumberFactory.crisp_number(0), FuzzyNumber)
    assert isinstance(FuzzyNumberFactory.crisp_number(0), FuzzyNumber)


def test_fuzzynumber_creation_string():
    string_fn = (
        "(0.0;1.0,3.0)(0.111111111111111;1.1,2.9)(0.222222222222222;1.2,2.8)(0.333333333333333;1.3,2.7)"
        "(0.444444444444444;1.4,2.6)(0.555555555555556;1.5,2.5)(0.666666666666667;1.6,2.4)"
        "(0.777777777777778;1.7,2.3)(0.888888888888889;1.8,2.2)(1.0;2.0,2.0)"
    )
    fn = FuzzyNumberFactory.parse_string(string_fn)

    assert isinstance(fn, FuzzyNumber)
    assert fn.min == Decimal(1)
    assert fn.max == Decimal(3)
    assert fn.kernel_min == Decimal(2)
    assert fn.kernel_max == Decimal(2)

    string_fn = "(0.0;1,3)(0.5;1.9999,2.0001)(1.0;2,2)"
    fn = FuzzyNumberFactory.parse_string(string_fn)

    assert isinstance(fn, FuzzyNumber)
    assert fn.get_alpha_cut(0.5).min == Decimal("1.9999")
    assert fn.get_alpha_cut(0.5).max == Decimal("2.0001")

    string_fn = "(0.0;1,3)(1.0;2,2)"
    fn = FuzzyNumberFactory.parse_string(string_fn)

    assert isinstance(fn, FuzzyNumber)
    assert fn == FuzzyNumberFactory.triangular(1, 2, 3)


def test_fuzzynumber_creation_string_errors():
    with pytest.raises(ValueError, match="Cannot parse FuzzyNumber from this definition"):
        string_fn = "(0.0;1.0,3.0)(0.5;1.9999)(1.0;2.0,2.0)"
        FuzzyNumberFactory.parse_string(string_fn)

    with pytest.raises(ValueError, match="element of Fuzzy Number"):
        string_fn = "(0.0;1.0,3.0)(0.5;2.0001,1.9999)(1.0;2.0,2.0)"
        FuzzyNumberFactory.parse_string(string_fn)

    with pytest.raises(ValueError, match="element of Fuzzy Number"):
        string_fn = "(0.0;1.0,3.0)(1.1;1.9999,2.0001)(1.0;2.0,2.0)"
        FuzzyNumberFactory.parse_string(string_fn)

    with pytest.raises(ValueError, match="Interval on lower alpha level has to contain the higher"):
        string_fn = "(0.0;1.0,3.0)(0.5;2.5,2.75)(1.0;2.0,2.0)"
        FuzzyNumberFactory.parse_string(string_fn)
