from decimal import Decimal

from FuzzyMath import FuzzyAnd, FuzzyMembership, FuzzyOr, PossibilisticAnd, PossibilisticMembership, PossibilisticOr


def test_fuzzy_and(quantize_precision):
    fm_a = FuzzyMembership("0.7")
    fm_b = FuzzyMembership("0.3")

    assert FuzzyAnd.min(fm_a, fm_b) == Decimal("0.3")
    assert FuzzyAnd.product(fm_a, fm_b) == Decimal("0.21")
    assert FuzzyAnd.drastic(fm_a, fm_b) == Decimal("0.0")
    assert FuzzyAnd.Lukasiewicz(fm_a, fm_b) == Decimal("0.0")
    assert FuzzyAnd.Nilpotent(fm_a, fm_b) == Decimal("0.0")
    assert FuzzyAnd.Hamacher(fm_a, fm_b).membership.quantize(quantize_precision) == Decimal(
        "0.265822784810127"
    ).quantize(quantize_precision)


def test_fuzzy_or(quantize_precision):
    fm_a = FuzzyMembership("0.7")
    fm_b = FuzzyMembership("0.3")

    assert FuzzyOr.max(fm_a, fm_b) == Decimal("0.7")
    assert FuzzyOr.product(fm_a, fm_b) == Decimal("0.79")
    assert FuzzyOr.drastic(fm_a, fm_b) == Decimal("0.0")
    assert FuzzyOr.Lukasiewicz(fm_a, fm_b) == Decimal("1.0")
    assert FuzzyOr.Nilpotent(fm_a, fm_b) == Decimal("1.0")
    assert FuzzyOr.Hamacher(fm_a, fm_b).membership.quantize(quantize_precision) == Decimal(0.826446280991736).quantize(
        quantize_precision
    )


def test_possibilistic_and(quantize_precision):
    pm_a = PossibilisticMembership("0.8", "0.5")
    pm_b = PossibilisticMembership("0.4", "0.2")

    assert PossibilisticAnd.min(pm_a, pm_b) == PossibilisticMembership("0.4", "0.2")
    assert PossibilisticAnd.product(pm_a, pm_b) == PossibilisticMembership("0.32", "0.1")
    assert PossibilisticAnd.drastic(pm_a, pm_b) == PossibilisticMembership("0.0", "0.0")
    assert PossibilisticAnd.Lukasiewicz(pm_a, pm_b) == PossibilisticMembership("0.2", "0.0")
    assert PossibilisticAnd.Nilpotent(pm_a, pm_b) == PossibilisticMembership("0.4", "0.0")
    assert PossibilisticAnd.Hamacher(pm_a, pm_b).possibility.quantize(quantize_precision) == Decimal(
        "0.363636363636364"
    ).quantize(quantize_precision)
    assert PossibilisticAnd.Hamacher(pm_a, pm_b).necessity.quantize(quantize_precision) == Decimal(
        "0.166666666666667"
    ).quantize(quantize_precision)


def test_possibilistic_or(quantize_precision):
    pm_a = PossibilisticMembership("0.8", "0.5")
    pm_b = PossibilisticMembership("0.4", "0.2")

    assert PossibilisticOr.max(pm_a, pm_b) == PossibilisticMembership("0.8", "0.5")
    assert PossibilisticOr.product(pm_a, pm_b) == PossibilisticMembership("0.88", "0.6")
    assert PossibilisticOr.drastic(pm_a, pm_b) == PossibilisticMembership("0.0", "0.0")
    assert PossibilisticOr.Lukasiewicz(pm_a, pm_b) == PossibilisticMembership("1.0", "0.7")
    assert PossibilisticOr.Nilpotent(pm_a, pm_b) == PossibilisticMembership("1.0", "0.5")
    assert PossibilisticOr.Hamacher(pm_a, pm_b).possibility.quantize(quantize_precision) == Decimal(
        "0.909090909090909"
    ).quantize(quantize_precision)
    assert PossibilisticOr.Hamacher(pm_a, pm_b).necessity.quantize(quantize_precision) == Decimal(
        "0.636363636363636"
    ).quantize(quantize_precision)
