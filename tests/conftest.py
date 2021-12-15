import pytest

from FuzzyMath import Interval, FuzzyNumber


@pytest.fixture
def i_a() -> Interval:
    return Interval.infimum_supremum(1, 3)


@pytest.fixture
def i_b() -> Interval:
    return Interval.infimum_supremum(2, 5)


@pytest.fixture
def i_c() -> Interval:
    return Interval.infimum_supremum(4, 7)


@pytest.fixture
def i_d() -> Interval:
    return Interval.infimum_supremum(-2, 3)


@pytest.fixture
def i_e() -> Interval:
    return Interval.infimum_supremum(-1, 1)


@pytest.fixture
def i_f() -> Interval:
    return Interval.empty()


@pytest.fixture
def fn_a() -> FuzzyNumber:
    return FuzzyNumber.triangular(1, 2, 3)


@pytest.fixture
def fn_b() -> FuzzyNumber:
    return FuzzyNumber.triangular(2, 3, 4)


@pytest.fixture
def fn_c() -> FuzzyNumber:
    return FuzzyNumber.triangular(-1, 0, 1)


@pytest.fixture
def fn_d() -> FuzzyNumber:
    return FuzzyNumber.trapezoidal(1, 2, 3, 4)


@pytest.fixture
def fn_e() -> FuzzyNumber:
    return FuzzyNumber.triangular(1, 2, 3, number_of_cuts=6)
