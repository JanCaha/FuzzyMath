from decimal import Decimal

import pytest

from FuzzyMath.class_factories import IntervalFactory
from FuzzyMath.class_interval import Interval
from FuzzyMath.class_precision import FuzzyMathPrecision


def test_creation_errors():
    with pytest.raises(ArithmeticError, match="`width` of interval must number higher or at least equal to 0."):
        IntervalFactory.midpoint_width(0, -1)

    with pytest.raises(ValueError, match="The interval is invalid. `minimum` must be lower or equal to `maximum`"):
        IntervalFactory.infimum_supremum(3, 1)

    with pytest.raises(ValueError, match="Cannot parse Interval from this definition"):
        IntervalFactory.parse_string("[1, 2.5, 5]")

    with pytest.raises(ValueError, match="Cannot parse Interval from this definition"):
        IntervalFactory.parse_string("[]")

    with pytest.raises(ValueError, match="Cannot parse Interval from this definition"):
        IntervalFactory.parse_string('["aa", "b"]')


def test_creation_with_precision():
    FuzzyMathPrecision.set_numeric_precision(2)

    interval = IntervalFactory.infimum_supremum("1.12345", "2.987")

    assert interval.min == Decimal("1.12")
    assert interval.max == Decimal("2.99")

    interval = IntervalFactory.infimum_supremum("1.1", "2.9")
    new_interval = interval + Decimal("0.001")

    assert new_interval == interval

    interval = IntervalFactory.infimum_supremum("1.1", "2.9")
    new_interval = interval + Decimal("0.09")

    assert new_interval == IntervalFactory.infimum_supremum("1.19", "2.99")

    FuzzyMathPrecision.unset_numeric_precision()


def test_creation():
    assert isinstance(IntervalFactory.infimum_supremum(1, 3), Interval)

    assert isinstance(IntervalFactory.infimum_supremum(2, 5), Interval)

    assert isinstance(IntervalFactory.infimum_supremum(4, 7), Interval)

    assert isinstance(IntervalFactory.infimum_supremum(-2, 3), Interval)

    assert isinstance(IntervalFactory.infimum_supremum(-1, 1), Interval)

    assert isinstance(IntervalFactory.empty(), Interval)

    interval = IntervalFactory.parse_string("[1, 2.5]")

    assert interval.min == Decimal("1")
    assert interval.max == Decimal("2.5")

    interval = IntervalFactory.infimum_supremum("0.1", "0.3")

    assert isinstance(interval, Interval)
    assert interval.min == Decimal("0.1")
    assert interval.max == Decimal("0.3")
