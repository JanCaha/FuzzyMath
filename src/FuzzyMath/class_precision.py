"""Classes handling precision"""
import typing
from decimal import Decimal


class FuzzyMathPrecision(object):
    """Object representing precision of FuzzyMath. Used in Interval and FuzzyNumber representation."""

    numeric_precision: typing.Optional[Decimal] = None
    alpha_precision: typing.Optional[Decimal] = None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(FuzzyMathPrecision, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def set_numeric_precision(decimal_places: int) -> None:
        """Set precision for numeric values - typically limits of Interval and thus Alpha cuts as well.

        Args:
            decimal_places (int): Number of decimal places to use.
        """
        FuzzyMathPrecision().numeric_precision = Decimal(10) ** -decimal_places

    @staticmethod
    def unset_numeric_precision() -> None:
        """Unset decimal places precision."""
        FuzzyMathPrecision().numeric_precision = None

    @staticmethod
    def set_alpha_precision(decimal_places: int) -> None:
        """Set alpha values precision.  Limits the precision of alpha values.

        Args:
            decimal_places (int): Number of decimal places to use for alpha cut values.
        """
        FuzzyMathPrecision().alpha_precision = Decimal(10) ** -decimal_places

    @staticmethod
    def unset_alpha_precision() -> None:
        """Unset decimal places for alpha precision."""
        FuzzyMathPrecision().alpha_precision = None

    @staticmethod
    def prepare_number(value: Decimal) -> Decimal:
        """Prepare number according to current settings of FuzzyMathPrecision.

        Args:
            value (Decimal): Input value.

        Returns:
            Decimal
        """
        fuzzy_precision = FuzzyMathPrecision()
        if fuzzy_precision.numeric_precision is None:
            return value
        else:
            return value.quantize(fuzzy_precision.numeric_precision)

    @staticmethod
    def reset() -> None:
        """
        Reset values of both numeric and alpha precision.
        """
        FuzzyMathPrecision().alpha_precision = None
        FuzzyMathPrecision().numeric_precision = None

    @staticmethod
    def prepare_alpha(value: Decimal) -> Decimal:
        """Prepare alpha value according to current settings of FuzzyMathPrecision.

        Args:
            value (Decimal): Input alpha value.

        Returns:
            Decimal
        """
        fuzzy_precision = FuzzyMathPrecision()
        if fuzzy_precision.alpha_precision is None:
            return value
        else:
            return value.quantize(fuzzy_precision.alpha_precision)


class FuzzyMathPrecisionContext:
    """
    Context for quickly and simply changing precision of FuzzyNumbers and Intervals.
    """

    def __init__(
        self, numeric_precision: typing.Optional[int] = None, alpha_precision: typing.Optional[int] = None
    ) -> None:
        self.numeric_precision = numeric_precision
        self.alpha_precision = alpha_precision

        self.previous_numeric_precision = FuzzyMathPrecision.numeric_precision
        self.previous_alpha_precision = FuzzyMathPrecision.alpha_precision

    def __enter__(self):
        if self.numeric_precision:
            FuzzyMathPrecision.set_numeric_precision(self.numeric_precision)
        if self.alpha_precision:
            FuzzyMathPrecision.set_alpha_precision(self.alpha_precision)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.previous_numeric_precision is None:
            FuzzyMathPrecision.unset_numeric_precision()
        else:
            FuzzyMathPrecision.set_numeric_precision(self.previous_numeric_precision)

        if self.previous_alpha_precision is None:
            FuzzyMathPrecision.unset_numeric_precision()
        else:
            FuzzyMathPrecision.set_alpha_precision(self.previous_alpha_precision)
