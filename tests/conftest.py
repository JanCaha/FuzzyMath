import pytest

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