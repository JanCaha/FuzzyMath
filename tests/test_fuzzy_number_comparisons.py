from conftest import assert_equal_decimals

from FuzzyMath import (
    FuzzyNumberFactory,
    PossibilisticMembership,
    exceedance,
    strict_exceedance,
    strict_undervaluation,
    undervaluation,
)


def test_comparison(quantize_precision):
    fn_a = FuzzyNumberFactory.triangular("0.2", "1.0", "2.8")
    fn_b = FuzzyNumberFactory.triangular("0.0", "1.8", "2.2")

    assert_equal_decimals(exceedance(fn_a, fn_b).possibility, "0.777777777777778", quantize_precision)
    assert_equal_decimals(exceedance(fn_a, fn_b).necessity, "0.384615384615385", quantize_precision)

    assert_equal_decimals(strict_exceedance(fn_a, fn_b).possibility, "0.454545454545455", quantize_precision)
    assert_equal_decimals(strict_exceedance(fn_a, fn_b).necessity, "0.0", quantize_precision)

    assert_equal_decimals(undervaluation(fn_a, fn_b).possibility, "1.0", quantize_precision)
    assert_equal_decimals(undervaluation(fn_a, fn_b).necessity, "0.545454545454545", quantize_precision)

    assert_equal_decimals(strict_undervaluation(fn_a, fn_b).possibility, "0.615384615384615", quantize_precision)
    assert_equal_decimals(strict_undervaluation(fn_a, fn_b).necessity, "0.222222222222222", quantize_precision)


def test_problematic_comparison():
    fn_a = FuzzyNumberFactory.triangular("0.2", "1.0", "2.8")
    fn_b = FuzzyNumberFactory.triangular("0.2", "1.8", "2.8")

    assert isinstance(exceedance(fn_a, fn_b), PossibilisticMembership)
    assert isinstance(strict_exceedance(fn_a, fn_b), PossibilisticMembership)
    assert isinstance(undervaluation(fn_a, fn_b), PossibilisticMembership)
    assert isinstance(strict_undervaluation(fn_a, fn_b), PossibilisticMembership)

    fn_a = FuzzyNumberFactory.triangular("0.2", "1.0", "2.8")
    fn_b = FuzzyNumberFactory.triangular("0.0", "1", "3")

    assert isinstance(exceedance(fn_a, fn_b), PossibilisticMembership)
    assert isinstance(strict_exceedance(fn_a, fn_b), PossibilisticMembership)
    assert isinstance(undervaluation(fn_a, fn_b), PossibilisticMembership)
    assert isinstance(strict_undervaluation(fn_a, fn_b), PossibilisticMembership)
