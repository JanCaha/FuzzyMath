import typing
from decimal import Decimal


class FuzzyMathPrecision(object):
    numeric_precision: typing.Optional[Decimal] = None
    alpha_precision: typing.Optional[Decimal] = None

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(FuzzyMathPrecision, cls).__new__(cls)
        return cls.instance

    @staticmethod
    def set_numeric_precision(decimal_places: int) -> None:
        FuzzyMathPrecision().numeric_precision = Decimal(10) ** -decimal_places

    @staticmethod
    def unset_numeric_precision() -> None:
        FuzzyMathPrecision().numeric_precision = None

    @staticmethod
    def set_alpha_precision(decimal_places: int) -> None:
        FuzzyMathPrecision().alpha_precision = Decimal(10) ** -decimal_places

    @staticmethod
    def unset_alpha_precision() -> None:
        FuzzyMathPrecision().alpha_precision = None

    @staticmethod
    def prepare_number(value: Decimal) -> Decimal:
        fuzzy_precision = FuzzyMathPrecision()
        if fuzzy_precision.numeric_precision is None:
            return value
        else:
            return value.quantize(fuzzy_precision.numeric_precision)

    @staticmethod
    def prepare_alpha(value: Decimal) -> Decimal:
        fuzzy_precision = FuzzyMathPrecision()
        if fuzzy_precision.alpha_precision is None:
            return value
        else:
            return value.quantize(fuzzy_precision.alpha_precision)
