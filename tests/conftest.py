import pytest
import typing

from decimal import Decimal

from FuzzyMath import Interval, FuzzyNumber, IntervalFactory, FuzzyNumberFactory


@pytest.fixture
def i_a() -> Interval:
    return IntervalFactory.infimum_supremum(1, 3)


@pytest.fixture
def i_b() -> Interval:
    return IntervalFactory.infimum_supremum(2, 5)


@pytest.fixture
def i_c() -> Interval:
    return IntervalFactory.infimum_supremum(4, 7)


@pytest.fixture
def i_d() -> Interval:
    return IntervalFactory.infimum_supremum(-2, 3)


@pytest.fixture
def i_e() -> Interval:
    return IntervalFactory.infimum_supremum(-1, 1)


@pytest.fixture
def i_f() -> Interval:
    return IntervalFactory.empty()


@pytest.fixture
def fn_a() -> FuzzyNumber:
    return FuzzyNumberFactory.triangular(1, 2, 3)


@pytest.fixture
def fn_b() -> FuzzyNumber:
    return FuzzyNumberFactory.triangular(2, 3, 4)


@pytest.fixture
def fn_c() -> FuzzyNumber:
    return FuzzyNumberFactory.triangular(-1, 0, 1)


@pytest.fixture
def fn_d() -> FuzzyNumber:
    return FuzzyNumberFactory.trapezoidal(1, 2, 3, 4)


@pytest.fixture
def fn_e() -> FuzzyNumber:
    return FuzzyNumberFactory.triangular(1, 2, 3, number_of_cuts=6)

@pytest.fixture
def quantize_precision() -> Decimal:
    return Decimal(10) ** -15

def assert_equal_decimals(a: Decimal, b: typing.Union[Decimal, str], quantize_precision: Decimal) -> None:
    if isinstance(b, str):
        b = Decimal(b)

    assert a.quantize(quantize_precision) == b.quantize(quantize_precision)