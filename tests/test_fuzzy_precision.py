from decimal import Decimal

from FuzzyMath import FuzzyMathPrecision


def test_is_singleton():
    fp_a = FuzzyMathPrecision()
    fp_a.set_numeric_precision(5)

    fp_b = FuzzyMathPrecision()

    assert fp_a is fp_b
    assert fp_a.numeric_precision == fp_b.numeric_precision

    assert fp_a.alpha_precision is None

    fp_b.set_alpha_precision(5)

    assert fp_a.alpha_precision is not None
    assert fp_a.alpha_precision == Decimal(10) ** -5


def test_unset():
    fp = FuzzyMathPrecision()

    alpha_prec = 2
    numeric_prec = 15

    fp.set_alpha_precision(alpha_prec)
    fp.set_numeric_precision(numeric_prec)

    assert fp.alpha_precision == Decimal(10) ** -alpha_prec
    assert fp.numeric_precision == Decimal(10) ** -numeric_prec

    fp.unset_alpha_precision()

    assert fp.alpha_precision is None

    fp.unset_numeric_precision()

    assert fp.numeric_precision is None


def test_precision():
    fp = FuzzyMathPrecision()

    alpha_prec = 2
    numeric_prec = 5

    fp.set_alpha_precision(alpha_prec)
    fp.set_numeric_precision(numeric_prec)

    value = Decimal("15.1234567")

    assert FuzzyMathPrecision.prepare_number(value) == value.quantize(Decimal(10) ** -numeric_prec)
    assert FuzzyMathPrecision.prepare_alpha(value) == value.quantize(Decimal(10) ** -alpha_prec)

    FuzzyMathPrecision.unset_alpha_precision()
    FuzzyMathPrecision.unset_numeric_precision()

    assert FuzzyMathPrecision.prepare_number(value) == value
    assert FuzzyMathPrecision.prepare_alpha(value) == value
