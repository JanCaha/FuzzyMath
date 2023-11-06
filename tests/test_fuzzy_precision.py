from decimal import Decimal

from FuzzyMath import FuzzyMathPrecision, FuzzyMathPrecisionContext, FuzzyNumberFactory, IntervalFactory


def to_decimal_precision(decimal_numbers: int) -> Decimal:
    return Decimal(10) ** -decimal_numbers


def test_is_singleton():
    fp_a = FuzzyMathPrecision()
    fp_a.set_numeric_precision(5)

    fp_b = FuzzyMathPrecision()

    assert fp_a is fp_b
    assert fp_a.numeric_precision == fp_b.numeric_precision

    assert fp_a.alpha_precision is None

    fp_b.set_alpha_precision(5)

    assert fp_a.alpha_precision is not None
    assert fp_a.alpha_precision == to_decimal_precision(5)


def test_unset():
    fp = FuzzyMathPrecision()

    alpha_prec = 2
    numeric_prec = 15

    fp.set_alpha_precision(alpha_prec)
    fp.set_numeric_precision(numeric_prec)

    assert fp.alpha_precision == to_decimal_precision(alpha_prec)
    assert fp.numeric_precision == to_decimal_precision(numeric_prec)

    fp.unset_alpha_precision()

    assert fp.alpha_precision is None

    fp.unset_numeric_precision()

    assert fp.numeric_precision is None


def test_interval_precision():
    fp = FuzzyMathPrecision()

    alpha_prec = 2
    numeric_prec = 5

    fp.set_alpha_precision(alpha_prec)
    fp.set_numeric_precision(numeric_prec)

    value = Decimal("15.1234567")

    assert FuzzyMathPrecision.prepare_number(value) == value.quantize(to_decimal_precision(numeric_prec))
    assert FuzzyMathPrecision.prepare_alpha(value) == value.quantize(to_decimal_precision(alpha_prec))

    FuzzyMathPrecision.unset_alpha_precision()
    FuzzyMathPrecision.unset_numeric_precision()

    assert FuzzyMathPrecision.prepare_number(value) == value
    assert FuzzyMathPrecision.prepare_alpha(value) == value


def test_math_precision_context():
    i_1 = IntervalFactory.two_values("1.12345", "2.98765")
    i_2 = IntervalFactory.two_values("1.12345", "2.98765")

    res = i_1 + i_2

    assert res == IntervalFactory.two_values("2.2469", "5.9753")

    with FuzzyMathPrecisionContext(1):
        assert FuzzyMathPrecision().alpha_precision is None
        assert FuzzyMathPrecision().numeric_precision == to_decimal_precision(1)
        res = i_1 + i_2

    assert res == IntervalFactory.two_values("2.2", "6.0")
    assert FuzzyMathPrecision().alpha_precision is None
    assert FuzzyMathPrecision().numeric_precision is None

    with FuzzyMathPrecisionContext(3):
        assert FuzzyMathPrecision().alpha_precision is None
        assert FuzzyMathPrecision().numeric_precision == to_decimal_precision(3)
        res = i_1 + i_2

    assert res == IntervalFactory.two_values("2.247", "5.975")
    assert FuzzyMathPrecision().alpha_precision is None
    assert FuzzyMathPrecision().numeric_precision is None


def test_fuzzy_number_precision():
    with FuzzyMathPrecisionContext(1, 2):
        fn_a = FuzzyNumberFactory.triangular("1.123", "2.123", "3.123", 7)

    assert fn_a.min == Decimal("1.1")
    assert fn_a.kernel_min == Decimal("2.1")
    assert fn_a.max == Decimal("3.1")

    assert fn_a.alpha_levels == [
        Decimal("0.00"),
        Decimal("0.17"),
        Decimal("0.33"),
        Decimal("0.50"),
        Decimal("0.67"),
        Decimal("0.83"),
        Decimal("1.00"),
    ]
