import pytest

from FuzzyMath import FuzzyMembership, PossibilisticMembership
from FuzzyMath import FuzzyAnd, FuzzyOr, PossibilisticAnd, PossibilisticOr

DIFF = 0.0000000001


def test_fuzzy_and():

    fm_a = FuzzyMembership(0.7)
    fm_b = FuzzyMembership(0.3)

    assert FuzzyAnd.min(fm_a, fm_b) == 0.3
    assert FuzzyAnd.product(fm_a, fm_b) == 0.21
    assert FuzzyAnd.drastic(fm_a, fm_b) == 0.0
    assert FuzzyAnd.Lukasiewicz(fm_a, fm_b) == 0.0
    assert FuzzyAnd.Nilpotent(fm_a, fm_b) == 0.0
    assert FuzzyAnd.Hamacher(fm_a, fm_b) == 0.265822784810127


def test_fuzzy_or():

    fm_a = FuzzyMembership(0.7)
    fm_b = FuzzyMembership(0.3)

    assert FuzzyOr.max(fm_a, fm_b) == 0.7
    assert FuzzyOr.product(fm_a, fm_b) == 0.79
    assert FuzzyOr.drastic(fm_a, fm_b) == 0.0
    assert FuzzyOr.Lukasiewicz(fm_a, fm_b) == 1.0
    assert FuzzyOr.Nilpotent(fm_a, fm_b) == 1.0
    assert FuzzyOr.Hamacher(fm_a, fm_b) == pytest.approx(0.826446280991736, DIFF)


def test_possibilistic_and():

    pm_a = PossibilisticMembership(0.8, 0.5)
    pm_b = PossibilisticMembership(0.4, 0.2)

    assert PossibilisticAnd.min(pm_a, pm_b) == PossibilisticMembership(0.4, 0.2)
    assert PossibilisticAnd.product(pm_a, pm_b) == PossibilisticMembership(0.32, 0.1)
    assert PossibilisticAnd.drastic(pm_a, pm_b) == PossibilisticMembership(0.0, 0.0)
    assert PossibilisticAnd.Lukasiewicz(pm_a, pm_b) == PossibilisticMembership(0.2, 0.0)
    assert PossibilisticAnd.Nilpotent(pm_a, pm_b) == PossibilisticMembership(0.4, 0.0)
    assert PossibilisticAnd.Hamacher(pm_a, pm_b) == PossibilisticMembership(0.363636363636364, 0.166666666666667)


def test_possibilistic_or():

    pm_a = PossibilisticMembership(0.8, 0.5)
    pm_b = PossibilisticMembership(0.4, 0.2)

    assert PossibilisticOr.max(pm_a, pm_b) == PossibilisticMembership(0.8, 0.5)
    assert PossibilisticOr.product(pm_a, pm_b) == PossibilisticMembership(0.88, 0.6)
    assert PossibilisticOr.drastic(pm_a, pm_b) == PossibilisticMembership(0.0, 0.0)
    assert PossibilisticOr.Lukasiewicz(pm_a, pm_b) == PossibilisticMembership(1.0, 0.7)
    assert PossibilisticOr.Nilpotent(pm_a, pm_b) == PossibilisticMembership(1.0, 0.5)
    assert PossibilisticOr.Hamacher(pm_a, pm_b) == PossibilisticMembership(0.909090909090909, 0.636363636363636)
