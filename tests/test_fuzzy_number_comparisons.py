from FuzzyMath import (FuzzyNumber, FuzzyNumberFactory, PossibilisticMembership, exceedance,
                       strict_exceedance, undervaluation, strict_undervaluation)


def test_comparison():

    fn_a = FuzzyNumberFactory.triangular(0.2, 1.0, 2.8)
    fn_b = FuzzyNumberFactory.triangular(0.0, 1.8, 2.2)

    assert exceedance(fn_a, fn_b).possibility == 0.777777777777778
    assert exceedance(fn_a, fn_b).necessity == 0.384615384615385

    assert strict_exceedance(fn_a, fn_b).possibility == 0.454545454545454
    assert strict_exceedance(fn_a, fn_b).necessity == 0.0

    assert undervaluation(fn_a, fn_b).possibility == 1.0
    assert undervaluation(fn_a, fn_b).necessity == 0.545454545454546

    assert strict_undervaluation(fn_a, fn_b).possibility == 0.615384615384615
    assert strict_undervaluation(fn_a, fn_b).necessity == 0.222222222222222


def test_problematic_comparison():

    fn_a = FuzzyNumberFactory.triangular(0.2, 1.0, 2.8)
    fn_b = FuzzyNumberFactory.triangular(0.2, 1.8, 2.8)

    assert isinstance(exceedance(fn_a, fn_b), PossibilisticMembership)
    assert isinstance(strict_exceedance(fn_a, fn_b), PossibilisticMembership)
    assert isinstance(undervaluation(fn_a, fn_b), PossibilisticMembership)
    assert isinstance(strict_undervaluation(fn_a, fn_b), PossibilisticMembership)

    fn_a = FuzzyNumberFactory.triangular(0.2, 1.0, 2.8)
    fn_b = FuzzyNumberFactory.triangular(0.0, 1, 3)

    assert isinstance(exceedance(fn_a, fn_b), PossibilisticMembership)
    assert isinstance(strict_exceedance(fn_a, fn_b), PossibilisticMembership)
    assert isinstance(undervaluation(fn_a, fn_b), PossibilisticMembership)
    assert isinstance(strict_undervaluation(fn_a, fn_b), PossibilisticMembership)
